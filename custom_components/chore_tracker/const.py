"""Constants for the Chore Tracker integration."""

DOMAIN = "chore_tracker"

# Repeat intervals
REPEAT_DAILY = "daily"
REPEAT_WEEKLY = "weekly"
REPEAT_BI_WEEKLY = "bi_weekly"
REPEAT_CUSTOM = "custom"

# Services
SERVICE_COMPLETE_CHORE = "complete_chore"
SERVICE_RESET_CHORE = "reset_chore"
SERVICE_ADD_CHORE = "add_chore"
SERVICE_REMOVE_CHORE = "remove_chore"

# Attributes
ATTR_CHORE_ID = "chore_id"
ATTR_CHORE_NAME = "chore_name"
ATTR_REPEAT_INTERVAL = "repeat_interval"
ATTR_CUSTOM_DAYS = "custom_days"
ATTR_TRIGGER_ENTITY = "trigger_entity"
ATTR_TRIGGER_STATE = "trigger_state"
ATTR_COMPLETED = "completed"
ATTR_LAST_COMPLETED = "last_completed"
ATTR_NEXT_DUE = "next_due"
