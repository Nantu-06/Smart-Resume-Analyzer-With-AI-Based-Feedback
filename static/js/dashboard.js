// ─── Dashboard Initialization ─────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Data injected by the inline <script> in dashboard.html before this file loads
  const data = window.__dashboardData;
  if (!data) return;
  initScoreRings(data);
  initBreakdownBars(data);
  initKeywords(data);
  initSections(data);
  initSuggestions(data);
});

function initScoreRings(data) {
  animateRing('resumeRing', data.resume_score || 0);
  animateRing('atsRing', data.ats_score || 0);

  // Set color class
  setScoreClass('resumeScoreCard', data.resume_score || 0);
  setScoreClass('atsScoreCard', data.ats_score || 0);
}

function animateRing(ringId, value) {
  const ring = document.getElementById(ringId);
  if (!ring) return;
  const circumference = 408; // 2 * PI * 65
  const offset = circumference - (value / 100) * circumference;
  setTimeout(() => {
    ring.style.strokeDashoffset = offset;
  }, 200);
}

function setScoreClass(cardId, score) {
  const card = document.getElementById(cardId);
  if (!card) return;
  card.classList.remove('score-excellent', 'score-good', 'score-average', 'score-poor');
  if (score >= 80) card.classList.add('score-excellent');
  else if (score >= 60) card.classList.add('score-good');
  else if (score >= 40) card.classList.add('score-average');
  else card.classList.add('score-poor');
}

function initBreakdownBars(data) {
  const container = document.getElementById('breakdownList');
  if (!container || !data.score_breakdown) return;

  const maxWeights = {
    education: 15, experience: 25, projects: 20,
    skills: 20, summary: 10, certifications: 5,
    contact: 5, contact_info: 5
  };

  container.innerHTML = '';
  Object.entries(data.score_breakdown || {}).forEach(([key, val]) => {
    if (key === 'contact_info') return; // rolled into contact display
    const max = maxWeights[key] || 10;
    const pct = max > 0 ? (val / max) * 100 : 0;
    const color = val > 0 ? 'var(--gradient-purple)' : 'rgba(248,113,113,0.4)';
    container.innerHTML += `
      <div class="breakdown-item">
        <div class="breakdown-header">
          <span class="breakdown-label">${key}</span>
          <span class="breakdown-score">${val}/${max}</span>
        </div>
        <div class="mini-bar-track">
          <div class="mini-bar-fill" data-pct="${pct}" style="background:${color}; width:0%"></div>
        </div>
      </div>`;
  });

  // Animate bars
  setTimeout(() => {
    container.querySelectorAll('.mini-bar-fill').forEach(bar => {
      bar.style.width = bar.dataset.pct + '%';
    });
  }, 300);
}

function initKeywords(data) {
  const found = data.found_keywords || [];
  const missing = data.missing_skills || [];

  const foundEl = document.getElementById('foundKeywords');
  const missingEl = document.getElementById('missingKeywords');

  if (foundEl) {
    foundEl.innerHTML = found.length
      ? found.map(k => `<span class="keyword-chip keyword-found">✓ ${k}</span>`).join('')
      : '<span style="color:var(--text-muted);font-size:.82rem">None found for this role.</span>';
  }
  if (missingEl) {
    missingEl.innerHTML = missing.length
      ? missing.map(k => `<span class="keyword-chip keyword-missing">✗ ${k}</span>`).join('')
      : '<span style="color:var(--accent-green);font-size:.82rem">🎉 All keywords present!</span>';
  }

  // Update counts
  const foundCount = document.getElementById('foundCount');
  const missingCount = document.getElementById('missingCount');
  if (foundCount) foundCount.textContent = `${found.length} found`;
  if (missingCount) missingCount.textContent = `${missing.length} missing`;
}

function initSections(data) {
  const allSections = ['summary', 'education', 'experience', 'projects', 'skills', 'certifications', 'contact'];
  const found = data.found_sections || [];
  const container = document.getElementById('sectionsList');
  if (!container) return;

  container.innerHTML = allSections.map(sec => {
    const isFound = found.includes(sec);
    return `
      <div class="section-row">
        <span class="section-name">${sec}</span>
        <span class="section-badge ${isFound ? 'badge-found' : 'badge-missing'}">
          ${isFound ? '✓ Present' : '✗ Missing'}
        </span>
      </div>`;
  }).join('');
}

function initSuggestions(data) {
  const suggestions = data.suggestions || [];
  const priorityMap = data.priority_map || {};
  const container = document.getElementById('suggestionsList');
  if (!container) return;

  if (!suggestions.length) {
    container.innerHTML = `<div style="color:var(--accent-green);text-align:center;padding:24px;">
      🎉 Excellent! Your resume is well-optimized.
    </div>`;
    return;
  }

  container.innerHTML = suggestions.map(s => {
    const pri = priorityMap[s] || 'low';
    const icons = { high: '🔴', medium: '🟡', low: '🟢' };
    return `
      <div class="suggestion-item priority-${pri}">
        <div class="suggestion-icon">${icons[pri]}</div>
        <span>${s}</span>
      </div>`;
  }).join('');
}
