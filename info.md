# Chore Tracker for Home Assistant

A futuristic, Iron Man/Tony Stark themed chore and task tracker for Home Assistant with automated triggers, repeating intervals, and motivational UI.

> *"Sir, your mission objectives are ready for review"* - JARVIS

## Features

- 🎯 **Manual and Automatic Triggers**: Mark chores complete manually or automatically based on device states
- 🔄 **Flexible Repeat Intervals**: Daily, weekly, bi-weekly, or custom interval chores
- 🦾 **Iron Man Themed UI**: Futuristic design with Arc Reactor animations and JARVIS-style notifications
- ✨ **Interactive Animations**: Pulsing effects, scanning lines, and completion celebrations
- 💪 **Motivational Messages**: Context-aware encouragement from JARVIS to keep you going
- 📊 **Progress Tracking**: Visual progress bars with real-time completion percentages

## Installation via HACS

1. Add this repository to HACS as a custom repository
2. Search for "Chore Tracker" in HACS
3. Click Install
4. Restart Home Assistant
5. Add the integration through the UI: Configuration → Integrations → Add Integration → Chore Tracker

## Installing the Custom Card

After installing the integration, you also need to install the custom Lovelace card:

1. Copy the `www/chore-tracker-card.js` file from this repository to your Home Assistant `www` directory
2. Add the resource to Lovelace:
   - Go to **Configuration** → **Lovelace Dashboards** → **Resources**
   - Click **+ Add Resource**
   - URL: `/local/chore-tracker-card.js`
   - Resource type: **JavaScript Module**
3. Clear browser cache (Ctrl+Shift+R)

## Quick Start

After installation, add a card to your dashboard:

```yaml
type: custom:chore-tracker-card
entity: sensor.daily_chores
title: Daily Mission Objectives
```

Then add chores using the `chore_tracker.add_chore` service:

```yaml
service: chore_tracker.add_chore
data:
  chore_id: "make_bed"
  chore_name: "Make Bed"
  repeat_interval: "daily"
```

## Available Services

- `chore_tracker.add_chore` - Add a new chore
- `chore_tracker.complete_chore` - Mark a chore as complete
- `chore_tracker.reset_chore` - Reset a chore to incomplete
- `chore_tracker.remove_chore` - Remove a chore from the list

## Available Sensors

After installation, you'll have these sensors:
- `sensor.daily_chores` - Daily chore list
- `sensor.weekly_chores` - Weekly chore list
- `sensor.bi_weekly_chores` - Bi-weekly chore list

## Documentation

For detailed configuration and usage instructions, see the [full documentation](https://github.com/boss0007000/automated-chore-tracker-list-tracker).
