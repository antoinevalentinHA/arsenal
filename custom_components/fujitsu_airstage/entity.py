"""Airstage parent entity class."""

from typing import Any

from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from pyairstage.airstageAC import AirstageAC
from pyairstage.airstageApi import ApiError

from .const import DOMAIN
from .models import AirstageData


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
        notify the coordinator's listeners. Every entity of the device then
        reflects the target immediately, and the next *scheduled* poll (well
        past the unit's convergence window) reconciles with the device without
        an early stale read. ``updates`` maps a ``pyairstage`` ``ACParameter``
        to its raw value; both are stringified to match the on-device format.
        """
        data = self.coordinator.data
        if not data or self.ac_key not in data:
            return

        wanted = {str(name): str(value) for name, value in updates.items()}
        for parameter in data[self.ac_key].get("parameters", []):
            name = parameter.get("name")
            if name in wanted:
                parameter["value"] = wanted[name]

        self.coordinator.async_update_listeners()

    @property
    def extra_state_attributes(self) -> dict:
        devices = self.instance.coordinator.data
        return {
            str(x["name"]).replace("iu_", ""): x["value"]
            for x in devices[self.ac_key]["parameters"]
        }
