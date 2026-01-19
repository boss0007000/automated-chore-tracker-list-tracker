# Feature Guide

## Overview

The Chore Tracker is a complete task management system for Home Assistant with a focus on making household chores fun and engaging through an Iron Man/Tony Stark themed interface.

## Core Components

### 1. Custom Integration (`custom_components/chore_tracker`)

The backend integration provides:
- **Three default sensors**: Daily, Weekly, and Bi-Weekly chore lists
- **Service calls** for chore management
- **State tracking** for each chore
- **Automatic reset** based on repeat intervals
- **Event listeners** for automated chore completion

### 2. Custom Lovelace Card (`www/chore-tracker-card.js`)

The frontend card features:
- **Futuristic UI** with Iron Man color scheme (gold, red, cyan)
- **Animated elements** (arc reactor, scan lines, progress bars)
- **Interactive chores** with click-to-complete functionality
- **JARVIS dialogue** that changes based on progress

## Detailed Features

### Manual Triggers

Click any chore in the card to toggle its completion status. The card will:
- ✅ Update the checkbox with a glow effect
- 📊 Animate the progress bar
- 💬 Update the JARVIS motivational message
- ✨ Apply visual effects (strike-through, scanning overlay)

**Service Call Example:**
```yaml
service: chore_tracker.complete_chore
data:
  chore_id: "make_bed"
```

### Automatic Triggers

Set up chores to automatically complete when a device reaches a specific state.

**Example - Auto-complete when vacuum docks:**
```yaml
service: chore_tracker.add_chore
data:
  chore_id: "vacuum_house"
  chore_name: "Vacuum House"
  repeat_interval: "daily"
  trigger_entity: "vacuum.robot_vacuum"
  trigger_state: "docked"
```

The integration monitors the specified entity and automatically marks the chore complete when it reaches the trigger state.

### Repeat Intervals

#### Daily Chores
- Reset every 24 hours
- Perfect for: making bed, washing dishes, feeding pets
- Sensor: `sensor.daily_chores`

```yaml
service: chore_tracker.add_chore
data:
  chore_id: "feed_pets"
  chore_name: "Feed Pets"
  repeat_interval: "daily"
```

#### Weekly Chores
- Reset every 7 days
- Perfect for: cleaning bathroom, vacuuming, grocery shopping
- Sensor: `sensor.weekly_chores`

```yaml
service: chore_tracker.add_chore
data:
  chore_id: "clean_bathroom"
  chore_name: "Clean Bathroom"
  repeat_interval: "weekly"
```

#### Bi-Weekly Chores
- Reset every 14 days
- Perfect for: deep cleaning, organizing, maintenance tasks
- Sensor: `sensor.bi_weekly_chores`

```yaml
service: chore_tracker.add_chore
data:
  chore_id: "deep_clean_kitchen"
  chore_name: "Deep Clean Kitchen"
  repeat_interval: "bi_weekly"
```

#### Custom Interval Chores
- Reset after X days (you specify)
- Perfect for: any custom schedule
- Can be added to any sensor list

```yaml
service: chore_tracker.add_chore
data:
  chore_id: "water_plants"
  chore_name: "Water Plants"
  repeat_interval: "custom"
  custom_days: 3
```

### Iron Man Theme Elements

#### Arc Reactor
- Pulsing cyan glow in top-right corner
- Breathes with energy (scales and fades)
- Multiple shadow layers for depth

#### Scanning Effects
- Animated scan line that moves down the card
- Gives active monitoring feel
- Cyan gradient for authenticity

#### Progress Bar
- Gradient fill from red to gold (Iron Man colors)
- Shimmer animation that sweeps across
- Real-time percentage display
- Smooth transitions when completing chores

#### JARVIS Dialogue
Context-aware messages based on completion percentage:
- **0%**: "Let's get started, Sir. The suit is ready."
- **1-24%**: "Good start, Sir. Keep the momentum going."
- **25-49%**: "Making progress, Sir. I'm impressed."
- **50-74%**: "Excellent work, Sir. We're more than halfway there."
- **75-99%**: "Almost there, Sir. Just a few more tasks."
- **100%**: "Mission accomplished, Sir. All systems complete. Outstanding work."

#### Chore Item Animations
- Hover effects with glow and slide
- Checkboxes that glow cyan when checked
- Strike-through text for completed items
- Scanning overlay on completed chores

### Interactive Features

#### Click to Complete
Simply click any chore item to toggle its status. The card communicates with Home Assistant to update the state.

#### Progress Tracking
Watch your progress in real-time:
- Visual progress bar fills as you complete tasks
- Percentage displayed prominently
- Completed/Total count shown

#### Visual Feedback
Every interaction provides feedback:
- Smooth animations
- Color changes
- Glow effects
- Position shifts

### Motivational System

The card uses psychology to encourage task completion:

1. **Visual Progress**: See your accomplishments grow
2. **Positive Reinforcement**: JARVIS praises your efforts
3. **Gamification**: Completing chores feels like completing missions
4. **Celebration**: Special message when everything is done
5. **Iron Man Theme**: Makes chores feel heroic and important

### Integration with Home Assistant

#### State Attributes
Each sensor provides rich state attributes:
```yaml
state: 2  # Number of completed chores
attributes:
  chores:
    - chore_id: "make_bed"
      chore_name: "Make Bed"
      completed: true
      last_completed: "2026-01-19T10:30:00"
      repeat_interval: "daily"
  completed_count: 2
  total_count: 5
  interval: "daily"
```

#### Services
- `chore_tracker.add_chore` - Add a new chore
- `chore_tracker.complete_chore` - Mark chore complete
- `chore_tracker.reset_chore` - Mark chore incomplete
- `chore_tracker.remove_chore` - Remove a chore

#### Automation Integration
Use chore completion to trigger other actions:

```yaml
automation:
  - alias: "Celebrate All Chores Done"
    trigger:
      platform: state
      entity_id: sensor.daily_chores
    condition:
      condition: template
      value_template: >
        {{ state_attr('sensor.daily_chores', 'completed_count') == 
           state_attr('sensor.daily_chores', 'total_count') }}
    action:
      - service: notify.mobile_app
        data:
          message: "All daily chores complete! 🎉"
```

## Advanced Usage

### Multiple Chore Lists

Create different cards for different areas:

```yaml
# Kitchen chores
type: custom:chore-tracker-card
entity: sensor.daily_chores
title: Kitchen Operations

# Bedroom chores  
type: custom:chore-tracker-card
entity: sensor.weekly_chores
title: Bedroom Maintenance
```

### Custom Notifications

Set up reminders and celebrations:

```yaml
# Evening reminder
automation:
  - alias: "Chore Reminder"
    trigger:
      platform: time
      at: "20:00:00"
    condition:
      condition: template
      value_template: >
        {{ state_attr('sensor.daily_chores', 'completed_count') < 
           state_attr('sensor.daily_chores', 'total_count') }}
    action:
      - service: notify.mobile_app
        data:
          title: "Pending Tasks"
          message: "You have unfinished chores, Sir."
```

### Integration with Smart Home Devices

Link chores to device states:

```yaml
# Dishwasher
service: chore_tracker.add_chore
data:
  chore_id: "run_dishwasher"
  chore_name: "Run Dishwasher"
  repeat_interval: "daily"
  trigger_entity: "sensor.dishwasher"
  trigger_state: "clean"

# Laundry
service: chore_tracker.add_chore
data:
  chore_id: "do_laundry"
  chore_name: "Do Laundry"
  repeat_interval: "weekly"
  trigger_entity: "sensor.washing_machine"
  trigger_state: "finished"
```

### Scripts for Bulk Operations

```yaml
script:
  weekend_chores:
    alias: "Add Weekend Chores"
    sequence:
      - service: chore_tracker.add_chore
        data:
          chore_id: "mow_lawn"
          chore_name: "Mow Lawn"
          repeat_interval: "weekly"
      - service: chore_tracker.add_chore
        data:
          chore_id: "wash_car"
          chore_name: "Wash Car"
          repeat_interval: "bi_weekly"
```

## Tips and Tricks

### Best Practices

1. **Use descriptive IDs**: Make chore_id values clear and consistent
2. **Group by frequency**: Use the appropriate sensor for each interval
3. **Set up automations**: Add chores automatically on HA start
4. **Link to devices**: Use automatic triggers when possible
5. **Create notifications**: Celebrate completions and remind about pending tasks

### Customization Ideas

1. **Color Scheme**: Modify CSS variables in the card for different themes
2. **Messages**: Edit JARVIS dialogue to match your preference
3. **Animations**: Adjust timing and effects in the CSS
4. **Layout**: Multiple cards for different rooms or people
5. **Rewards**: Trigger lights, sounds, or other effects on completion

### Troubleshooting

**Chores disappear after restart**
- Chores are stored in memory only
- Set up an automation to re-add them on HA start
- This is by design for flexibility

**Card doesn't update**
- Clear browser cache
- Check that the card can access the entity
- Verify the resource is loaded

**Auto-complete not working**
- Verify entity ID is correct
- Check that state matches exactly (case-sensitive)
- Ensure the entity actually changes to that state

## Future Enhancements

Potential features for future versions:
- Persistent storage for chores
- Multiple user support with profiles
- Points/rewards system
- Statistics and history
- Mobile app integration
- Voice control through JARVIS
- Custom animations per chore type
- Integration with calendar
- Task dependencies
- Recurring exceptions (skip holidays)

## Contributing

Contributions are welcome! Areas to improve:
- Additional themes
- More animation effects
- Better mobile responsiveness
- Performance optimizations
- Additional automation examples
- Localization support

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review example configurations
- Test with the demo.html file

---

Made with ❤️ and inspired by Tony Stark's JARVIS
