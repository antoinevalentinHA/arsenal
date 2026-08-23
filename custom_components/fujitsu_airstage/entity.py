"""Airstage parent entity class."""

from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

import aiohttp
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from pyairstage.airstageAC import AirstageAC
from pyairstage.airstageApi import ApiError

from .const import DOMAIN
from .models import AirstageData

# Transport failures a write command can surface when the indoor unit drops off
# the LAN (Wi-Fi loss, unit unplugged, module rebooting).
#   - ``ApiError``      : pyairstage gave up after its own retries.
#   - ``aiohttp`` errors: leak straight through when pyairstage does not wrap
#     them (``ClientConnectorError`` also derives from ``OSError``, but
#     ``ClientError`` as a whole does not).
#   - ``OSError``       : raw socket failures, and ``TimeoutError``, which is an
#     ``OSError`` subclass since Python 3.10.
# ``asyncio.CancelledError`` derives from ``BaseException`` and is therefore
# never swallowed here — a stopped script must still stop.
_COMMAND_TRANSPORT_ERRORS = (ApiError, aiohttp.ClientError, OSError)


def airstage_command(
    func: Callable[..., Awaitable[Any]],
) -> Callable[..., Awaitable[Any]]:
    """Surface a write command's transport failures as ``HomeAssistantError``.

    Without this, an unreachable unit raises ``pyairstage`` / ``aiohttp``
    exceptions straight out of the service call. Home Assistant classifies
    those as *unexpected*: the caller gets a full traceback in the log, and —
    decisively — the failure escapes ``continue_on_error``, which by design
    only ever swallows ``HomeAssistantError``. Any script commanding the unit
    is then aborted mid-sequence, skipping whatever bookkeeping followed
    (post-condition check, failure marking, scheduled retry).

    Translating the failure keeps the same command *failing* — nothing is
    silently ignored — but as an error Home Assistant understands: logged
    without a stack trace, and containable by the caller. Read paths are not
    concerned: they serve the coordinator cache, whose own failures are
    already mapped to ``UpdateFailed``.
    """

    @wraps(func)
    async def _wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except HomeAssistantError:
            # Already translated (typically by a nested decorated command).
            raise
        except _COMMAND_TRANSPORT_ERRORS as err:
            raise HomeAssistantError(
                f"Airstage command {func.__name__} failed: {err}"
            ) from err

    return _wrapper


class AirstageEntity(CoordinatorEntity):
    """Parent class for Airstage Entities."""

    _attr_has_entity_name = True

    def __init__(self, instance: AirstageData) -> None:
        """Initialize common aspects of an Airstage entity."""
        super().__init__(instance.coordinator)
        # self._attr_unique_id: str = self.coordinator.data["system"]["rid"]

    def update_handle_factory(self, func, *keys):
        """Return the provided API function wrapped.

        Adds an error handler and coordinator refresh, and presets keys.
        """

        async def update_handle(*values):
            try:
                if await func(*keys, *values):
                    await self.coordinator.async_refresh()
            except ApiError as err:
                raise HomeAssistantError(err) from err

        return update_handle


class AirstageAcEntity(AirstageEntity):
    """Parent class for Airstage AC Entities."""

    def __init__(self, instance: AirstageData, ac_key: str) -> None:
        """Initialize common aspects of an Airstage ac entity."""
        super().__init__(instance)
        self.instance = instance

        self.ac_key: str = ac_key
        self._attr_unique_id = f"{ac_key}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            manufacturer="Fujitsu Airstage",
            model=self.coordinator.data[self.ac_key]["model"],
            name=self.coordinator.data[self.ac_key]["deviceName"],
        )

        self.async_update_ac = self.update_handle_factory(instance.api.get_devices)

    @property
    def _ac(self) -> AirstageAC:
        return AirstageAC(self.ac_key, self.instance.api).refresh_parameters(
            data=self.coordinator.data[self.ac_key]
        )

    def apply_optimistic_update(self, updates: dict[Any, Any]) -> None:
        """Reflect just-written parameters locally without an immediate re-poll.

        The Airstage API is eventually consistent (``iot_class:
        local_polling``): for up to a poll interval after a write the unit
        keeps reporting its *previous* value. Calling
        ``coordinator.async_refresh()`` straight after a write therefore reads
        the stale value back — and for the fan speed that resurfaces the
        manufacturer ``auto``. When an external automation reasserts the
        commanded speed on seeing ``auto``, the two race into a tight
        write → stale-read → rewrite loop (visible flapping, API hammering).

        Instead we patch the commanded values into the coordinator's cached
        ``parameters`` list — the source ``_ac`` rebuilds its state from — and
        publish them. Every entity of the device then reflects the target
        immediately, and the next *scheduled* poll (well past the unit's
        convergence window) reconciles with the device without an early stale
        read. ``updates`` maps a ``pyairstage`` ``ACParameter`` to its raw
        value; both are stringified to match the on-device format.

        Stringification is load-bearing and relies on Python 3.11+ enum
        semantics: ``ACParameter`` is a ``StrEnum`` (``str()`` yields
        ``"iu_fan_spd"``) and ``FanSpeed`` / ``BooleanProperty`` are
        ``IntEnum`` (``str()`` yields ``"2"`` / ``"1"``). On <= 3.10 these
        would render as ``"FanSpeed.QUIET"`` and silently poison the cache.

        Publishing goes through ``async_set_updated_data`` rather than
        ``async_update_listeners`` so the poll timer is *reset*: the former
        unsubscribes the pending refresh and reschedules a full interval.
        Without it a write landing seconds before an already-scheduled poll
        would still be read back stale — the very race this avoids, only
        rarer. It also forces ``last_update_success = True``, so it is only
        used when the coordinator is already healthy; while the device is
        unreachable we fall back to notifying listeners, which reflects the
        command without claiming an availability we have not verified.
        """
        data = self.coordinator.data
        if not data or self.ac_key not in data:
            return

        wanted = {str(name): str(value) for name, value in updates.items()}
        for parameter in data[self.ac_key].get("parameters", []):
            name = parameter.get("name")
            if name in wanted:
                parameter["value"] = wanted[name]

        if self.coordinator.last_update_success:
            self.coordinator.async_set_updated_data(data)
        else:
            self.coordinator.async_update_listeners()

    @property
    def extra_state_attributes(self) -> dict:
        devices = self.instance.coordinator.data
        return {
            str(x["name"]).replace("iu_", ""): x["value"]
            for x in devices[self.ac_key]["parameters"]
        }
