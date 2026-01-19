"""Sensor platform for Chore Tracker."""
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event
import homeassistant.util.dt as dt_util

from .const import (
    DOMAIN,
    REPEAT_DAILY,
    REPEAT_WEEKLY,
    REPEAT_BI_WEEKLY,
    REPEAT_CUSTOM,
    ATTR_CHORE_ID,
    ATTR_CHORE_NAME,
    ATTR_REPEAT_INTERVAL,
    ATTR_CUSTOM_DAYS,
    ATTR_TRIGGER_ENTITY,
    ATTR_TRIGGER_STATE,
    ATTR_COMPLETED,
    ATTR_LAST_COMPLETED,
    ATTR_NEXT_DUE,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Chore Tracker sensor platform."""
    # Create a chore list manager
    manager = ChoreListManager(hass)
    hass.data[DOMAIN][entry.entry_id] = manager
    
    # Register services
    await manager.async_register_services()
    
    # Create default chore lists
    entities = [
        ChoreListSensor(hass, manager, "daily", "Daily Chores"),
        ChoreListSensor(hass, manager, "weekly", "Weekly Chores"),
        ChoreListSensor(hass, manager, "bi_weekly", "Bi-Weekly Chores"),
    ]
    
    async_add_entities(entities, True)


class ChoreListManager:
    """Manage chore lists and chores."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the manager."""
        self.hass = hass
        self.chores: Dict[str, Dict[str, Any]] = {}
        self.listeners = []

    async def async_register_services(self):
        """Register services."""
        from homeassistant.helpers import config_validation as cv
        import voluptuous as vol
        from .const import (
            SERVICE_COMPLETE_CHORE,
            SERVICE_RESET_CHORE,
            SERVICE_ADD_CHORE,
            SERVICE_REMOVE_CHORE,
        )

        async def complete_chore_service(call):
            """Handle complete chore service."""
            chore_id = call.data.get(ATTR_CHORE_ID)
            await self.complete_chore(chore_id)

        async def reset_chore_service(call):
            """Handle reset chore service."""
            chore_id = call.data.get(ATTR_CHORE_ID)
            await self.reset_chore(chore_id)

        async def add_chore_service(call):
            """Handle add chore service."""
            chore_data = {
                ATTR_CHORE_ID: call.data.get(ATTR_CHORE_ID),
                ATTR_CHORE_NAME: call.data.get(ATTR_CHORE_NAME),
                ATTR_REPEAT_INTERVAL: call.data.get(ATTR_REPEAT_INTERVAL, REPEAT_DAILY),
                ATTR_CUSTOM_DAYS: call.data.get(ATTR_CUSTOM_DAYS),
                ATTR_TRIGGER_ENTITY: call.data.get(ATTR_TRIGGER_ENTITY),
                ATTR_TRIGGER_STATE: call.data.get(ATTR_TRIGGER_STATE),
                ATTR_COMPLETED: False,
                ATTR_LAST_COMPLETED: None,
            }
            await self.add_chore(chore_data)

        async def remove_chore_service(call):
            """Handle remove chore service."""
            chore_id = call.data.get(ATTR_CHORE_ID)
            await self.remove_chore(chore_id)

        self.hass.services.async_register(
            DOMAIN,
            SERVICE_COMPLETE_CHORE,
            complete_chore_service,
            schema=vol.Schema({vol.Required(ATTR_CHORE_ID): cv.string}),
        )

        self.hass.services.async_register(
            DOMAIN,
            SERVICE_RESET_CHORE,
            reset_chore_service,
            schema=vol.Schema({vol.Required(ATTR_CHORE_ID): cv.string}),
        )

        self.hass.services.async_register(
            DOMAIN,
            SERVICE_ADD_CHORE,
            add_chore_service,
            schema=vol.Schema({
                vol.Required(ATTR_CHORE_ID): cv.string,
                vol.Required(ATTR_CHORE_NAME): cv.string,
                vol.Optional(ATTR_REPEAT_INTERVAL, default=REPEAT_DAILY): cv.string,
                vol.Optional(ATTR_CUSTOM_DAYS): cv.positive_int,
                vol.Optional(ATTR_TRIGGER_ENTITY): cv.entity_id,
                vol.Optional(ATTR_TRIGGER_STATE): cv.string,
            }),
        )

        self.hass.services.async_register(
            DOMAIN,
            SERVICE_REMOVE_CHORE,
            remove_chore_service,
            schema=vol.Schema({vol.Required(ATTR_CHORE_ID): cv.string}),
        )

    async def add_chore(self, chore_data: Dict[str, Any]):
        """Add a new chore."""
        chore_id = chore_data[ATTR_CHORE_ID]
        self.chores[chore_id] = chore_data
        
        # Set up automatic trigger if specified
        if chore_data.get(ATTR_TRIGGER_ENTITY):
            self._setup_auto_trigger(chore_id, chore_data)
        
        await self._notify_listeners()

    async def remove_chore(self, chore_id: str):
        """Remove a chore."""
        if chore_id in self.chores:
            del self.chores[chore_id]
            await self._notify_listeners()

    async def complete_chore(self, chore_id: str):
        """Mark a chore as completed."""
        if chore_id in self.chores:
            self.chores[chore_id][ATTR_COMPLETED] = True
            self.chores[chore_id][ATTR_LAST_COMPLETED] = dt_util.now().isoformat()
            await self._notify_listeners()

    async def reset_chore(self, chore_id: str):
        """Reset a chore to incomplete."""
        if chore_id in self.chores:
            self.chores[chore_id][ATTR_COMPLETED] = False
            await self._notify_listeners()

    def _setup_auto_trigger(self, chore_id: str, chore_data: Dict[str, Any]):
        """Set up automatic trigger for chore completion."""
        trigger_entity = chore_data.get(ATTR_TRIGGER_ENTITY)
        trigger_state = chore_data.get(ATTR_TRIGGER_STATE)

        @callback
        def state_changed(event):
            """Handle state change."""
            new_state = event.data.get("new_state")
            if new_state and new_state.state == trigger_state:
                self.hass.async_create_task(self.complete_chore(chore_id))

        listener = async_track_state_change_event(
            self.hass, trigger_entity, state_changed
        )
        self.listeners.append(listener)

    async def _notify_listeners(self):
        """Notify all sensors to update."""
        # This will be called by sensors when they need updates
        pass

    def get_chores_by_interval(self, interval: str) -> list:
        """Get all chores for a specific interval."""
        return [
            chore for chore in self.chores.values()
            if chore.get(ATTR_REPEAT_INTERVAL) == interval
        ]

    def calculate_next_due(self, chore: Dict[str, Any]) -> Optional[datetime]:
        """Calculate when a chore is next due."""
        last_completed = chore.get(ATTR_LAST_COMPLETED)
        if not last_completed:
            return dt_util.now()
        
        last_completed_dt = dt_util.parse_datetime(last_completed)
        interval = chore.get(ATTR_REPEAT_INTERVAL)
        
        if interval == REPEAT_DAILY:
            return last_completed_dt + timedelta(days=1)
        elif interval == REPEAT_WEEKLY:
            return last_completed_dt + timedelta(days=7)
        elif interval == REPEAT_BI_WEEKLY:
            return last_completed_dt + timedelta(days=14)
        elif interval == REPEAT_CUSTOM:
            custom_days = chore.get(ATTR_CUSTOM_DAYS, 1)
            return last_completed_dt + timedelta(days=custom_days)
        
        return None


class ChoreListSensor(SensorEntity):
    """Representation of a Chore List sensor."""

    def __init__(self, hass: HomeAssistant, manager: ChoreListManager, interval: str, name: str):
        """Initialize the sensor."""
        self._hass = hass
        self._manager = manager
        self._interval = interval
        self._attr_name = name
        self._attr_unique_id = f"chore_tracker_{interval}"
        self._attr_icon = "mdi:format-list-checks"
        self._state = 0
        self._chores = []

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "chores": self._chores,
            "completed_count": sum(1 for c in self._chores if c.get(ATTR_COMPLETED)),
            "total_count": len(self._chores),
            "interval": self._interval,
        }

    async def async_update(self):
        """Update the sensor."""
        self._chores = self._manager.get_chores_by_interval(self._interval)
        
        # Check if any chores need to be reset based on their interval
        now = dt_util.now()
        for chore in self._chores:
            next_due = self._manager.calculate_next_due(chore)
            if next_due and now >= next_due and chore.get(ATTR_COMPLETED):
                await self._manager.reset_chore(chore[ATTR_CHORE_ID])
        
        # Update state
        completed_count = sum(1 for c in self._chores if c.get(ATTR_COMPLETED))
        self._state = completed_count
