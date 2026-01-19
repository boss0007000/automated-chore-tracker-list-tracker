# Installation Guide

## Installation Methods

Choose one of the following methods to install Chore Tracker:

### Method 1: HACS Installation (Recommended)

1. **Install HACS** if you haven't already: [HACS Installation](https://hacs.xyz/docs/setup/download)

2. **Add Custom Repository**:
   - In HACS, go to **Integrations**
   - Click the **three dots** in the top right corner
   - Select **Custom repositories**
   - Add `https://github.com/boss0007000/automated-chore-tracker-list-tracker` as repository
   - Select **Integration** as category
   - Click **Add**

3. **Install Chore Tracker**:
   - Search for **Chore Tracker** in HACS
   - Click on it
   - Click **Download**
   - Restart Home Assistant

4. **Continue to Step 2** below to add the integration

### Method 2: Manual Installation

1. **Download or Clone** this repository
2. **Copy** the `custom_components/chore_tracker` folder to your Home Assistant config directory
   - Path should be: `<config>/custom_components/chore_tracker/`
3. **Restart** Home Assistant

## Step 2: Add the Integration

1. Go to **Configuration** → **Integrations**
2. Click the **+ Add Integration** button
3. Search for **Chore Tracker**
4. Click on it to add
5. Click **Submit** on the configuration dialog

## Step 3: Install the Custom Card

1. **Copy** the `www/chore-tracker-card.js` file to your Home Assistant www directory
   - Path should be: `<config>/www/chore-tracker-card.js`
   
2. **Add the resource** to Lovelace:
   - Go to **Configuration** → **Lovelace Dashboards** → **Resources**
   - Click **+ Add Resource**
   - URL: `/local/chore-tracker-card.js`
   - Resource type: **JavaScript Module**
   - Click **Create**

3. **Clear browser cache** (important!)
   - Press Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

## Step 4: Add Cards to Your Dashboard

1. Edit your Lovelace dashboard
2. Add a new card
3. Choose **Manual** card type
4. Paste this YAML:

```yaml
type: custom:chore-tracker-card
entity: sensor.daily_chores
title: Daily Mission Objectives
```

5. Save the card

## Step 5: Add Chores

You can add chores in several ways:

### Method 1: Using Developer Tools

1. Go to **Developer Tools** → **Services**
2. Service: `chore_tracker.add_chore`
3. Service Data:
```yaml
chore_id: "make_bed"
chore_name: "Make Bed"
repeat_interval: "daily"
```
4. Click **Call Service**

### Method 2: Using Automations

Create an automation that runs on Home Assistant start:

```yaml
automation:
  - alias: "Setup My Chores"
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
          chore_id: "clean_kitchen"
          chore_name: "Clean Kitchen"
          repeat_interval: "daily"
```

### Method 3: Using Scripts

Create a script for easy chore management:

```yaml
script:
  setup_chores:
    alias: "Setup All Chores"
    sequence:
      - service: chore_tracker.add_chore
        data:
          chore_id: "daily_task_1"
          chore_name: "My Daily Task"
          repeat_interval: "daily"
```

## Step 6: Verify Everything Works

1. Check that you see three sensor entities:
   - `sensor.daily_chores`
   - `sensor.weekly_chores`
   - `sensor.bi_weekly_chores`

2. Check that the card displays properly with the Iron Man theme

3. Try clicking a chore to mark it complete

4. Verify the animations and JARVIS messages appear

## Troubleshooting

### Card doesn't show up
- Clear browser cache (Ctrl+Shift+R)
- Make sure the resource is added correctly
- Check browser console for errors (F12)

### Services don't appear
- Restart Home Assistant
- Check `custom_components/chore_tracker/` exists
- Check Home Assistant logs for errors

### Chores don't save
- This is normal - chores are stored in memory
- Add them via automation on Home Assistant start
- Or use a future version with persistent storage

## Next Steps

1. Customize your chore lists
2. Set up automations for automatic chore completion
3. Create notifications for completed chores
4. Enjoy your Iron Man themed chore tracker!

## Need Help?

- Check the [README.md](../README.md) for full documentation
- Review the [examples/configuration.yaml](../examples/configuration.yaml) for configuration ideas
- Open an issue on GitHub if you find bugs
