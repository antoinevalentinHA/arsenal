import base64
import logging
from datetime import datetime, timedelta, timezone
from json import loads as json_loads
from zoneinfo import ZoneInfo
import aiohttp
from aiohttp.client import ClientTimeout, ClientError
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from .const import AUTH_URL, DATA_URL, API_GOUV_URL, URL_CODE

# Applied to every request. 120s used to be declared here and passed nowhere,
# so a hung connection could tie a coordinator up indefinitely.
DEFAULT_TIMEOUT = 30
CLIENT_TIMEOUT = ClientTimeout(total=DEFAULT_TIMEOUT)

# Only used when the token carries no readable expiry. Observed against the
# live API: it returns a JWT whose exp sits 24h out, so _jwt_expiry answers and
# this fallback is not normally reached. It stays as a net in case the token
# format changes, and must comfortably exceed REFRESH_INTERVALL: below it, the
# token would always be stale by the time the coordinator polls and the cache
# would buy nothing. Being optimistic is safe: a token refused early comes back
# as a 401, which get_data retries after re-authenticating.
TOKEN_DEFAULT_TTL = timedelta(hours=12)
# Renew slightly early so a token cannot expire in flight.
TOKEN_EXPIRY_MARGIN = timedelta(seconds=60)

_LOGGER = logging.getLogger(__name__)


def _jwt_expiry(token) -> datetime | None:
    """Read the `exp` claim of a JWT without pulling in a JWT dependency.

    Returns None for anything that is not a decodable JWT with a usable `exp`;
    callers then fall back to TOKEN_DEFAULT_TTL. The signature is not verified,
    which is fine here: the claim is only used to decide when to re-login.
    """
    try:
        payload_b64 = token.split(".")[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)
        exp = json_loads(base64.urlsafe_b64decode(payload_b64))["exp"]
        return datetime.fromtimestamp(exp, tz=timezone.utc)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError, OverflowError, OSError):
        _LOGGER.debug("Token carries no readable expiry, using default TTL")
        return None


class TooManyRequestsError(Exception):
    """Exception to handle too many requests error."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class InvalidAuthError(Exception):
    """The credentials were rejected.

    Kept distinct from every other login failure: this is the only one the
    user can do something about, and the only one worth interrupting them for.
    """


class AtmoFranceDataApi:
    """Api to get AirAtmo data"""

    def __init__(
        self,
        config,
        session: aiohttp.ClientSession = None,
        timeout=CLIENT_TIMEOUT,
        hass: HomeAssistant = None,
    ) -> None:
        self._timeout = timeout
        if session is not None:
            self._session = session
        else:
            self._session = aiohttp.ClientSession()
        self._config = config
        self._token = None
        self._token_expiry = None
        self._data = None
        self._hass = hass

    def _invalidate_token(self):
        """Forget the cached token so the next call logs in again."""
        self._token = None
        self._token_expiry = None

    async def async_get_token(self):
        """Get a user token, reusing the cached one until it nears expiry.

        Logging in on every single request is what gets this account rate
        limited (HTTP 429) by the Atmo France API.
        """
        if (
            self._token is not None
            and self._token_expiry is not None
            and datetime.now(timezone.utc) < self._token_expiry - TOKEN_EXPIRY_MARGIN
        ):
            _LOGGER.debug(
                "Reusing cached token, valid until %s", self._token_expiry)
            return

        self._invalidate_token()
        request = await self._session.post(
            AUTH_URL,
            json={
                "username": self._config[CONF_USERNAME],
                "password": self._config[CONF_PASSWORD],
            },
            timeout=self._timeout,
        )
        if request.status == 200:
            resp = await request.json()
            self._token = resp["token"]
            self._token_expiry = _jwt_expiry(self._token) or (
                datetime.now(timezone.utc) + TOKEN_DEFAULT_TTL
            )
            # `resp` holds the bearer token, never log it as-is.
            _LOGGER.debug("Got a new token, valid until %s",
                          self._token_expiry)
        elif request.status == 429:
            raise TooManyRequestsError(
                f"Too many requests response from the server, please retry in {request.headers.get("Retry-After")} seconds")
        elif request.status in (401, 403):
            raise InvalidAuthError(
                f"Atmo France rejected the credentials with status {request.status}"
            )
        else:
            raise ConnectionRefusedError(
                f"Failed to get authent token, with error status : {request.status}"
            )

    async def get_data(self, insee_code, url_code: URL_CODE) -> dict:
        """Get Data from AtmoFrance API"""
        today = datetime.now(
            ZoneInfo(self._hass.config.time_zone)).strftime("%Y-%m-%d")
        url = f'{DATA_URL}/{url_code.value}/{{"code_zone":{{"operator":"=","value":"{
            insee_code}"}},"date_ech":{{"operator":">=","value":"{today}"}}}}?withGeom=false'

        # Two attempts at most: the second one only happens when a cached token
        # is refused earlier than its announced expiry.
        for attempt in (1, 2):
            try:
                await self.async_get_token()
            except ConnectionRefusedError as err:
                _LOGGER.error(
                    "Failed to get token with status error %s ", err)
                return None
            except TooManyRequestsError as err:
                _LOGGER.error(
                    "Too many request error from the server. Try again in %s ", err)
                return None
            except (ClientError, TimeoutError) as err:
                _LOGGER.warning(
                    "Failed to reach the authentication endpoint: %s: %s",
                    type(err).__name__, err)
                return None

            headers = {"Authorization": f"Bearer {self._token}"}
            _LOGGER.debug("Getting data from %s", url)
            try:
                result = await self._session.get(
                    url, headers=headers, timeout=self._timeout)
                if result.status in (401, 403) and attempt == 1:
                    _LOGGER.debug(
                        "Token rejected with status %s, renewing it", result.status)
                    self._invalidate_token()
                    continue
                payload = await result.json()
            except (ClientError, TimeoutError) as err:
                # Le type compte autant que le message : TimeoutError et
                # plusieurs exceptions aiohttp ont un str() vide, et la ligne
                # se réduisait alors à « Failed to get data for INSEE X: ».
                # Warning et non error : le coordinateur lève UpdateFailed
                # juste après, que HA journalise déjà en erreur.
                _LOGGER.warning(
                    "Failed to get data for INSEE %s: %s: %s",
                    insee_code, type(err).__name__, err)
                return None
            break

        _LOGGER.debug("Got response %s ", payload)
        _LOGGER.debug(
            "Extracting data for INSEE %s and date %s", insee_code, today)
        features = payload.get("features") if isinstance(
            payload, dict) else None
        if features is None:  # unexpected payload (error page, quota, ...)
            _LOGGER.error(
                "Unexpected response from AtmoFrance API for INSEE %s: %s",
                insee_code,
                payload,
            )
            return None
        if len(features) > 0:  # At least one result
            self._data = payload
            _LOGGER.debug(
                "Got data for INSEE %s and date > %s: %s",
                insee_code,
                today,
                self._data,
            )
        else:  # no result
            self._data = None
            _LOGGER.warning(
                "No data for INSEE %s and date %s", insee_code, today)
        return features

    def get_key_value(self, key, shift: int = 0):
        """Get value for the given key in JSON Data for a given date based on shift from today"""
        extractDate = (datetime.now(
            ZoneInfo(self._hass.config.time_zone))+timedelta(days=shift)).strftime("%Y-%m-%d")
        if self._data is not None:
            extractedData = next(
                filter(
                    lambda feat: feat["properties"]["date_ech"] == extractDate,
                    self._data["features"],
                ), {"properties": {key: ""}})  # If not found return ''
            return extractedData.get("properties")[key]
        else:
            return ""

    @property
    def source(self):
        """Get value for source of data"""
        if self._data is not None:
            # Take the first value, we have multiple ones for forecast
            return self._data["features"][0]["properties"]["source"]
        return ""

    @property
    def last_update(self):
        """Get value of data update"""
        if self._data is not None:
            # Take the first value, we have multiple ones for forecast
            return self._data["features"][0]["properties"]["date_maj"]
        return ""

    @property
    def type_zone(self):
        """Get type of zone"""
        if self._data is not None:
            # Take the first value, we have multiple ones for forecast
            return self._data["features"][0]["properties"]["type_zone"]
        return ""

    @property
    def nom_zone(self):
        """Get Name of Zone"""
        if self._data is not None:
            # Take the first value, we have multiple ones for forecast
            return self._data["features"][0]["properties"]["lib_zone"]
        return ""


class INSEEAPI:
    """Api to get INSEE data"""

    def __init__(
        self, session: aiohttp.ClientSession = None, timeout=CLIENT_TIMEOUT
    ) -> None:
        self._timeout = timeout
        if session is not None:
            self._session = session
        else:
            self._session = aiohttp.ClientSession()

    async def get_data(self, zipcode) -> dict:
        """Get INSEE code for a given zip code"""
        url = f"{API_GOUV_URL}codePostal={
            zipcode}&fields=code,nom,codeEpci&format=json&geometry=centre"
        result = await self._session.get(url, timeout=self._timeout)
        if result.status == 200:
            json = await result.json()
            _LOGGER.debug("Got response for INSEE Code %s ", json)
            if len(json) == 0:
                _LOGGER.error("No INSEE value fetched for %s ", zipcode)
                raise ValueError
            return json
        else:
            _LOGGER.error(
                "Failed to get INSEE data, with status %s ", result.status)
            raise ValueError
