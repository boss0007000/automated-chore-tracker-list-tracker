# Chore Tracker for Home Assistant

A futuristic, Iron Man/Tony Stark themed chore and task tracker for Home Assistant with automated triggers, repeating intervals, and motivational UI.

![Chore Tracker Demo](https://github.com/user-attachments/assets/1903f84a-d300-4dd5-baf3-a7e51b09653a)

> *"Sir, your mission objectives are ready for review"* - JARVIS

## Features

- 🎯 **Manual and Automatic Triggers**: Mark chores complete manually or automatically based on device states
- 🔄 **Flexible Repeat Intervals**: Daily, weekly, bi-weekly, or custom interval chores
- 🦾 **Iron Man Themed UI**: Futuristic design with Arc Reactor animations and JARVIS-style notifications
- ✨ **Interactive Animations**: Pulsing effects, scanning lines, and completion celebrations
- 💪 **Motivational Messages**: Context-aware encouragement from JARVIS to keep you going
- 📊 **Progress Tracking**: Visual progress bars with real-time completion percentages

## Quick Start

1. **Install the integration** by copying `custom_components/chore_tracker` to your Home Assistant config
2. **Install the card** by copying `www/chore-tracker-card.js` to your www folder
3. **Restart Home Assistant** and add the integration via UI
4. **Add the card** to your dashboard with entity `sensor.daily_chores`
5. **Start adding chores** using the `chore_tracker.add_chore` service

See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions.

## Installation

### Manual Installation

1. Copy the `custom_components/chore_tracker` folder to your Home Assistant `custom_components` directory
2. Copy the `www/chore-tracker-card.js` file to your Home Assistant `www` directory
3. Restart Home Assistant
4. Add the integration through the UI: Configuration → Integrations → Add Integration → Chore Tracker

### Adding the Custom Card

Add this to your Lovelace resources (Configuration → Lovelace Dashboards → Resources):

```yaml
url: /local/chore-tracker-card.js
type: module
```

## Configuration

### Adding Chores via Services

You can add chores using the `chore_tracker.add_chore` service:

```yaml
service: chore_tracker.add_chore
data:
  chore_id: "vacuum_living_room"
  chore_name: "Vacuum Living Room"
  repeat_interval: "daily"
```

#### With Automatic Trigger

Set chores to auto-complete when a device reaches a certain state:

```yaml
service: chore_tracker.add_chore
data:
  chore_id: "dishwasher_run"
  chore_name: "Run Dishwasher"
  repeat_interval: "daily"
  trigger_entity: "sensor.dishwasher"
  trigger_state: "completed"
```

#### Custom Repeat Interval

```yaml
service: chore_tracker.add_chore
data:
  chore_id: "water_plants"
  chore_name: "Water Plants"
  repeat_interval: "custom"
  custom_days: 3
```

### Available Repeat Intervals

- `daily` - Resets every day
- `weekly` - Resets every 7 days
- `bi_weekly` - Resets every 14 days
- `custom` - Resets after specified number of days (requires `custom_days` parameter)

### Manual Control Services

**Complete a chore:**
```yaml
service: chore_tracker.complete_chore
data:
  chore_id: "vacuum_living_room"
```

**Reset a chore:**
```yaml
service: chore_tracker.reset_chore
data:
  chore_id: "vacuum_living_room"
```

**Remove a chore:**
```yaml
service: chore_tracker.remove_chore
data:
  chore_id: "vacuum_living_room"
```

## Lovelace Card Configuration

Add the card to your dashboard:

```yaml
type: custom:chore-tracker-card
entity: sensor.daily_chores
title: Daily Mission Objectives
```

### Available Entities

After installation, you'll have these sensors:
- `sensor.daily_chores` - Daily chore list
- `sensor.weekly_chores` - Weekly chore list
- `sensor.bi_weekly_chores` - Bi-weekly chore list

### Multiple Cards

You can create multiple cards for different chore lists:

```yaml
type: vertical-stack
cards:
  - type: custom:chore-tracker-card
    entity: sensor.daily_chores
    title: Daily Operations
  
  - type: custom:chore-tracker-card
    entity: sensor.weekly_chores
    title: Weekly Maintenance
  
  - type: custom:chore-tracker-card
    entity: sensor.bi_weekly_chores
    title: Bi-Weekly Systems Check
```

## Example Automation Setup

### Add Daily Chores on Home Assistant Start

```yaml
automation:
  - alias: "Setup Daily Chores"
    trigger:
      platform: homeassistant
      event: start
    action:
      - service: chore_tracker.add_chore
        data:
          chore_id: "make_bed"
          chore_name: "Make Bed"
          repeat_interval: "daily"
      
      - service: chore_tracker.add_chore
        data:
          chore_id: "wash_dishes"
          chore_name: "Wash Dishes"
          repeat_interval: "daily"
          trigger_entity: "binary_sensor.dishwasher"
          trigger_state: "off"
      
      - service: chore_tracker.add_chore
        data:
          chore_id: "take_out_trash"
          chore_name: "Take Out Trash"
          repeat_interval: "daily"
```

### Add Weekly Chores

```yaml
automation:
  - alias: "Setup Weekly Chores"
    trigger:
      platform: homeassistant
      event: start
    action:
      - service: chore_tracker.add_chore
        data:
          chore_id: "clean_bathroom"
          chore_name: "Clean Bathroom"
          repeat_interval: "weekly"
      
      - service: chore_tracker.add_chore
        data:
          chore_id: "vacuum_house"
          chore_name: "Vacuum Entire House"
          repeat_interval: "weekly"
          trigger_entity: "vacuum.robovac"
          trigger_state: "docked"
      
      - service: chore_tracker.add_chore
        data:
          chore_id: "change_sheets"
          chore_name: "Change Bed Sheets"
          repeat_interval: "weekly"
```

### Notify When Chores Are Complete

```yaml
automation:
  - alias: "Celebrate Chore Completion"
    trigger:
      platform: state
      entity_id: sensor.daily_chores
    condition:
      condition: template
      value_template: >
        {{ state_attr('sensor.daily_chores', 'completed_count') == 
           state_attr('sensor.daily_chores', 'total_count') and
           state_attr('sensor.daily_chores', 'total_count') > 0 }}
    action:
      - service: notify.mobile_app
        data:
          title: "🎉 Mission Complete!"
          message: "All daily chores completed! JARVIS is impressed, Sir."
```

## UI Features

### Arc Reactor Animation
- Pulsing blue arc reactor in the top-right corner
- Glowing effects that breathe with energy

### Progress Bar
- Animated gradient fill (red to gold)
- Shimmer effect that moves across the bar
- Real-time percentage display

### Chore Items
- Hover effects with glow and slide animations
- Checkboxes with smooth transitions
- Scanning line effect on completed items
- Strike-through text for completed chores

### JARVIS Voice
- Context-aware motivational messages
- Different messages based on completion percentage
- Iron Man/Tony Stark style dialogue

### Scanning Effects
- Animated scan line moving down the card
- Gives the feeling of active monitoring
- Futuristic HUD aesthetic

## Customization

The card uses CSS variables that can be customized:

```css
--iron-man-gold: #FFD700
--iron-man-red: #DC143C
--iron-man-dark: #1a1a2e
--iron-man-accent: #00D9FF
--stark-white: #FFFFFF
```

## Troubleshooting

### Card Not Showing
1. Make sure the resource is added in Lovelace resources
2. Clear browser cache
3. Restart Home Assistant

### Services Not Available
1. Ensure the integration is installed in `custom_components/chore_tracker`
2. Check Home Assistant logs for errors
3. Restart Home Assistant

### Chores Not Auto-Completing
1. Verify the trigger entity ID is correct
2. Check that the trigger state matches exactly
3. Ensure the entity state actually changes to the specified value

## Credits

Created with ❤️ for Home Assistant users who want to make chore tracking fun and futuristic!

Inspired by Tony Stark's JARVIS interface from Iron Man.

## License

MIT License - Feel free to use and modify as needed.