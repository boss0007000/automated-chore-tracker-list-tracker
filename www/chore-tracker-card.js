class ChoreTrackerCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._chores = [];
    this._config = {};
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this._config = config;
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  render() {
    if (!this._hass || !this._config.entity) {
      return;
    }

    const entity = this._hass.states[this._config.entity];
    if (!entity) {
      this.shadowRoot.innerHTML = `
        <ha-card>
          <div class="card-content">Entity not found: ${this._config.entity}</div>
        </ha-card>
      `;
      return;
    }

    const chores = entity.attributes.chores || [];
    const completedCount = entity.attributes.completed_count || 0;
    const totalCount = entity.attributes.total_count || 0;
    const interval = entity.attributes.interval || 'daily';

    const completionPercentage = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          --iron-man-gold: #FFD700;
          --iron-man-red: #DC143C;
          --iron-man-dark: #1a1a2e;
          --iron-man-accent: #00D9FF;
          --stark-white: #FFFFFF;
        }

        ha-card {
          background: linear-gradient(135deg, var(--iron-man-dark) 0%, #16213e 100%);
          border: 2px solid var(--iron-man-gold);
          border-radius: 16px;
          box-shadow: 0 0 30px rgba(255, 215, 0, 0.3), 
                      0 0 60px rgba(220, 20, 60, 0.2);
          overflow: hidden;
          position: relative;
        }

        .arc-reactor {
          position: absolute;
          top: 10px;
          right: 10px;
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background: radial-gradient(circle, var(--iron-man-accent) 0%, transparent 70%);
          box-shadow: 0 0 20px var(--iron-man-accent),
                      0 0 40px var(--iron-man-accent),
                      inset 0 0 10px var(--iron-man-accent);
          animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
          0%, 100% {
            opacity: 1;
            transform: scale(1);
          }
          50% {
            opacity: 0.7;
            transform: scale(1.1);
          }
        }

        .card-header {
          padding: 20px;
          background: linear-gradient(90deg, var(--iron-man-red) 0%, var(--iron-man-gold) 100%);
          color: var(--stark-white);
          font-size: 24px;
          font-weight: bold;
          text-transform: uppercase;
          letter-spacing: 2px;
          text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
          position: relative;
        }

        .jarvis-voice {
          font-size: 12px;
          font-style: italic;
          opacity: 0.9;
          margin-top: 5px;
          letter-spacing: 1px;
        }

        .progress-container {
          padding: 20px;
          position: relative;
        }

        .progress-bar {
          width: 100%;
          height: 30px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 15px;
          overflow: hidden;
          border: 1px solid var(--iron-man-accent);
          position: relative;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, var(--iron-man-red) 0%, var(--iron-man-gold) 100%);
          transition: width 0.5s ease-in-out;
          box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
          position: relative;
          overflow: hidden;
        }

        .progress-fill::before {
          content: '';
          position: absolute;
          top: 0;
          left: -100%;
          width: 100%;
          height: 100%;
          background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
          animation: shine 2s infinite;
        }

        @keyframes shine {
          0% { left: -100%; }
          100% { left: 100%; }
        }

        .progress-text {
          text-align: center;
          margin-top: 10px;
          color: var(--iron-man-gold);
          font-weight: bold;
          font-size: 18px;
          text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        }

        .chores-list {
          padding: 0 20px 20px 20px;
        }

        .chore-item {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 215, 0, 0.3);
          border-radius: 8px;
          padding: 15px;
          margin-bottom: 10px;
          display: flex;
          align-items: center;
          transition: all 0.3s ease;
          cursor: pointer;
          position: relative;
          overflow: hidden;
        }

        .chore-item:hover {
          background: rgba(255, 215, 0, 0.1);
          border-color: var(--iron-man-gold);
          transform: translateX(5px);
          box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
        }

        .chore-item.completed {
          background: rgba(0, 217, 255, 0.1);
          border-color: var(--iron-man-accent);
        }

        .chore-item.completed::after {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(90deg, transparent, rgba(0, 217, 255, 0.2), transparent);
          animation: scan 2s infinite;
        }

        @keyframes scan {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }

        .checkbox {
          width: 24px;
          height: 24px;
          border: 2px solid var(--iron-man-gold);
          border-radius: 4px;
          margin-right: 15px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: transparent;
          transition: all 0.3s ease;
        }

        .checkbox.checked {
          background: var(--iron-man-accent);
          border-color: var(--iron-man-accent);
          box-shadow: 0 0 15px var(--iron-man-accent);
        }

        .checkbox.checked::after {
          content: '✓';
          color: white;
          font-size: 18px;
          font-weight: bold;
        }

        .chore-name {
          flex: 1;
          color: var(--stark-white);
          font-size: 16px;
          text-decoration: none;
        }

        .chore-item.completed .chore-name {
          text-decoration: line-through;
          opacity: 0.7;
        }

        .motivation-message {
          padding: 15px 20px;
          text-align: center;
          color: var(--iron-man-gold);
          font-size: 16px;
          font-style: italic;
          border-top: 1px solid rgba(255, 215, 0, 0.3);
          animation: fadeIn 1s ease-in;
        }

        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        .no-chores {
          padding: 40px 20px;
          text-align: center;
          color: var(--iron-man-gold);
          font-size: 18px;
          font-style: italic;
        }

        .scan-line {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 2px;
          background: linear-gradient(90deg, transparent, var(--iron-man-accent), transparent);
          animation: scanLine 3s linear infinite;
        }

        @keyframes scanLine {
          0% { transform: translateY(0); }
          100% { transform: translateY(500px); }
        }
      </style>

      <ha-card>
        <div class="scan-line"></div>
        <div class="arc-reactor"></div>
        
        <div class="card-header">
          ${this._config.title || entity.attributes.friendly_name || 'Chore Tracker'}
          <div class="jarvis-voice">
            "Sir, your ${interval} objectives require attention"
          </div>
        </div>

        <div class="progress-container">
          <div class="progress-bar">
            <div class="progress-fill" style="width: ${completionPercentage}%"></div>
          </div>
          <div class="progress-text">
            ${completedCount} / ${totalCount} Complete (${Math.round(completionPercentage)}%)
          </div>
        </div>

        ${chores.length > 0 ? `
          <div class="chores-list">
            ${chores.map(chore => this.renderChore(chore)).join('')}
          </div>
        ` : `
          <div class="no-chores">
            "All systems operational. No pending tasks, Sir."
          </div>
        `}

        ${this.renderMotivation(completionPercentage)}
      </ha-card>
    `;

    // Add click handlers
    this.shadowRoot.querySelectorAll('.chore-item').forEach((item, index) => {
      item.addEventListener('click', () => this.toggleChore(chores[index]));
    });
  }

  renderChore(chore) {
    const completed = chore.completed || false;
    const name = chore.chore_name || chore.chore_id || 'Unnamed Chore';
    
    return `
      <div class="chore-item ${completed ? 'completed' : ''}" data-chore-id="${chore.chore_id}">
        <div class="checkbox ${completed ? 'checked' : ''}"></div>
        <div class="chore-name">${name}</div>
      </div>
    `;
  }

  renderMotivation(percentage) {
    let message = '';
    
    if (percentage === 0) {
      message = '"Let\'s get started, Sir. The suit is ready."';
    } else if (percentage < 25) {
      message = '"Good start, Sir. Keep the momentum going."';
    } else if (percentage < 50) {
      message = '"Making progress, Sir. I\'m impressed."';
    } else if (percentage < 75) {
      message = '"Excellent work, Sir. We\'re more than halfway there."';
    } else if (percentage < 100) {
      message = '"Almost there, Sir. Just a few more tasks."';
    } else {
      message = '"Mission accomplished, Sir. All systems complete. Outstanding work."';
    }

    return `<div class="motivation-message">${message}</div>`;
  }

  toggleChore(chore) {
    const service = chore.completed ? 'reset_chore' : 'complete_chore';
    
    this._hass.callService('chore_tracker', service, {
      chore_id: chore.chore_id
    });
  }

  getCardSize() {
    return 4;
  }
}

customElements.define('chore-tracker-card', ChoreTrackerCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'chore-tracker-card',
  name: 'Chore Tracker Card',
  description: 'An Iron Man themed chore tracker card with animations'
});
