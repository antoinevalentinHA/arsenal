""" Implements the sensors component """
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.device_registry import DeviceEntryType

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from .const import (
    DOMAIN,
    ATTRIBUTION,
    POLLUTION_SENSORS,
    POLLUTION_FORECAST_DAYS,
    POLLEN_ALERT_SENSORS,
    POLLEN_CONC_SENSORS,
    POLLEN_FORECAST_DAYS,
    CONF_CITY,
    CONF_INSEE_CODE,
    CONF_INCLUDE_POLLEN,
    CONF_INCLUDE_POLLEN_FORECAST,
    CONF_INCLUDE_POLLUTION,
    CONF_INCLUDE_POLLUTION_FORECAST,
    CONF_POLLUTION_COORDINATOR,
    CONF_POLLEN_COORDINATOR,
    POLLUTION_LEVEL,
    POLLEN_LEVEL,
    LEVEL_COLOR,
    MODEL,
    TITLE,
    AtmoFranceSensorEntityDescription,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Configuration"""
    config = hass.data[DOMAIN][entry.entry_id]
    entities = []

    if entry.options.get(CONF_INCLUDE_POLLUTION, False):
        coordinatorpollution = config[CONF_POLLUTION_COORDINATOR]
        for sensor_description in POLLUTION_SENSORS:
            entities.append(
                AtmoFrancePollutionEntity(hass, entry, sensor_description,
                                          coordinatorpollution))

    if entry.options.get(CONF_INCLUDE_POLLUTION_FORECAST, False):
        coordinatorpollution = config[CONF_POLLUTION_COORDINATOR]
        for shift in range(1, POLLUTION_FORECAST_DAYS + 1):
            for sensor_description in POLLUTION_SENSORS:
                entities.append(
                    AtmoFrancePollutionEntity(hass, entry, sensor_description,
                                              coordinatorpollution, shift))

    if entry.options.get(CONF_INCLUDE_POLLEN, False):
        coordinatorpollen = config[CONF_POLLEN_COORDINATOR]
        for sensor_description in POLLEN_ALERT_SENSORS:
            entities.append(AtmoFrancePollenLevelEntity(
                hass, entry, sensor_description, coordinatorpollen))
        for sensor_description in POLLEN_CONC_SENSORS:
            entities.append(AtmoFrancePollenConcentrationEntity(
                hass, entry, sensor_description, coordinatorpollen))

    if entry.options.get(CONF_INCLUDE_POLLEN_FORECAST, False):
        coordinatorpollen = config[CONF_POLLEN_COORDINATOR]
        for shift in range(1, POLLEN_FORECAST_DAYS + 1):
            for sensor_description in POLLEN_ALERT_SENSORS:
                entities.append(AtmoFrancePollenLevelEntity(
                    hass, entry, sensor_description, coordinatorpollen, shift))
            for sensor_description in POLLEN_CONC_SENSORS:
                entities.append(AtmoFrancePollenConcentrationEntity(
                    hass, entry, sensor_description, coordinatorpollen, shift))

    async_add_entities(entities, True)


class AtmoFranceEntity(CoordinatorEntity, SensorEntity):
    """La classe de l'entité Air Atmo"""

    entity_description: AtmoFranceSensorEntityDescription
    # The device carries the city, so entity names must not repeat it. The
    # unique_id is unchanged, so existing entities keep their entity_id and
    # their history; only the displayed name changes.
    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        entry_infos,
        description: SensorEntityDescription,
        coordinator,
    ) -> None:
        """Initisalisation de l'entité"""
        super().__init__(coordinator)

        self._hass = hass
        self.entity_description = description
        self._attr_name = description.name
        self._attr_unique_id = f"{
            entry_infos.entry_id}-{entry_infos.data.get(CONF_INSEE_CODE)}-{description.name}"
        self._device_id = entry_infos.entry_id
        self._coordinator = coordinator
        self._attr_attribution = f"{
            ATTRIBUTION}- {self._coordinator.api.source}"
        self._attr_device_class = description.device_class

        self._attr_device_info = DeviceInfo(
            name=f"{TITLE} - {entry_infos.data.get(CONF_CITY)}",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, f"{coordinator.api.source}-{entry_infos.data.get(CONF_CITY)}")
                         },
            manufacturer=f"{ATTRIBUTION}-{coordinator.api.source}",
            model=MODEL,
        )
        _LOGGER.debug("In base entity Creating an atmo France sensor, named %s",
                      self._attr_name)

    def _raw_value(self):
        """Read the raw API value, or None when it is not published yet."""
        raw = self._coordinator.api.get_key_value(
            self.entity_description.json_key, self._shift)
        if raw == "" or raw is None:
            # Nothing to warn about: forecasts are published during the day,
            # so J+1 is legitimately missing every morning.
            _LOGGER.debug("No value available yet for %s", self._attr_name)
            return None
        return raw

    def _level2color(self, value):
        return LEVEL_COLOR.get(value)


class AtmoFrancePollutionEntity(AtmoFranceEntity):
    def __init__(self, hass, entry_infos, description, coordinator, shift: int = 0):
        super().__init__(hass, entry_infos, description, coordinator)
        self._shift = shift

        if (self._shift > 0):
            self._attr_name = f"{description.name} J+{self._shift}"
            self._attr_unique_id = f"{
                entry_infos.entry_id}-{entry_infos.data.get(CONF_INSEE_CODE)}-{description.name}-J+{self._shift}"

        _LOGGER.debug("In AtmoFranceAlertEntity Creating an atmo France sensor, named %s",
                      self._attr_name)

    @property
    def native_value(self):
        raw = self._raw_value()
        if raw is None:
            return None
        try:
            value = int(raw)
        except (TypeError, ValueError):
            _LOGGER.warning("Unexpected value %r for %s",
                            raw, self._attr_name)
            return None
        _LOGGER.debug("Value for pollution sensor %s is now %s",
                      self._attr_name, value)
        return value

    @property
    def extra_state_attributes(self):
        value = self.native_value
        return {
            "Date de mise à jour": self._coordinator.api.last_update,
            "Libellé": self._level2string(value),
            "Couleur": self._level2color(value),
            "Type de zone": self._coordinator.api.type_zone,
            "Nom de la zone": self._coordinator.api.nom_zone,
        }

    def _level2string(self, value):
        return POLLUTION_LEVEL.get(value)


class AtmoFrancePollenLevelEntity(AtmoFranceEntity):
    def __init__(self, hass, entry_infos, description, coordinator, shift: int = 0):
        super().__init__(hass, entry_infos, description, coordinator)
        self._shift = shift

        if (self._shift > 0):
            self._attr_name = f"{description.name} J+{self._shift}"
            self._attr_unique_id = f"{
                entry_infos.entry_id}-{entry_infos.data.get(CONF_INSEE_CODE)}-{description.name}-J+{self._shift}"

        _LOGGER.debug("In AtmoFrancePollenLevelEntity Creating an atmo France sensor, named %s",
                      self._attr_name)

    @property
    def native_value(self):
        raw = self._raw_value()
        if raw is None:
            return None
        try:
            # Pollen alert levels are expressed as float cast them to int.
            value = int(raw)
        except (TypeError, ValueError):
            _LOGGER.warning("Unexpected value %r for %s",
                            raw, self._attr_name)
            return None
        _LOGGER.debug("Value for pollen level sensor %s is now %s",
                      self._attr_name, value)
        return value

    @property
    def extra_state_attributes(self):
        value = self.native_value
        return {
            "Date de mise à jour": self._coordinator.api.last_update,
            "Libellé": self._level2string(value),
            "Couleur": self._level2color(value),
            "Type de zone": self._coordinator.api.type_zone,
            "Nom de la zone": self._coordinator.api.nom_zone,
        }

    def _level2string(self, value):
        return POLLEN_LEVEL.get(value)


class AtmoFrancePollenConcentrationEntity(AtmoFranceEntity):
    def __init__(self, hass, entry_infos, description, coordinator, shift: int = 0):
        super().__init__(hass, entry_infos, description, coordinator)
        self._shift = shift

        if (self._shift > 0):
            self._attr_name = f"{description.name} J+{self._shift}"
            self._attr_unique_id = f"{
                entry_infos.entry_id}-{entry_infos.data.get(CONF_INSEE_CODE)}-{description.name}-J+{self._shift}"
        _LOGGER.debug("In AtmoFrancePollenEntity Creating an atmo France sensor, named %s",
                      self._attr_name)

    @property
    def native_value(self):
        # A real 0 is a valid concentration and must reach the state machine;
        # only an absent value becomes None.
        value = self._raw_value()
        _LOGGER.debug("Value for sensor %s is now %s",
                      self._attr_name, value)
        return value

    @property
    def extra_state_attributes(self):
        return {
            "Date de mise à jour": self._coordinator.api.last_update,
            "Type de zone": self._coordinator.api.type_zone,
            "Nom de la zone": self._coordinator.api.nom_zone,
        }
