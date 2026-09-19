// ─── Drag & Drop File Handling ───────────────────────────
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('resumeFile');
const selectedFileEl = document.getElementById('selectedFile');
const fileNameEl = document.getElementById('fileName');
const fileSizeEl = document.getElementById('fileSize');
const analyzeBtn = document.getElementById('analyzeBtn');
const form = document.getElementById('uploadForm');
const progressEl = document.getElementById('analysisProgress');
const progressFill = document.getElementById('progressFill');
const progressSteps = document.querySelectorAll('.progress-step');

let selectedFile = null;

// Drag events
['dragenter', 'dragover'].forEach(evt =>
  dropzone.addEventListener(evt, e => {
    e.preventDefault();
    dropzone.classList.add('drag-over');
  })
);
['dragleave', 'drop'].forEach(evt =>
  dropzone.addEventListener(evt, e => {
    e.preventDefault();
    dropzone.classList.remove('drag-over');
  })
);
dropzone.addEventListener('drop', e => {
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});

// Click-to-browse
fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) handleFile(fileInput.files[0]);
});

function handleFile(file) {
  const ext = file.name.split('.').pop().toLowerCase();
  if (!['pdf', 'docx'].includes(ext)) {
    showToast('⚠️ Only PDF and DOCX files are supported.');
    return;
  }
  selectedFile = file;
  fileNameEl.textContent = file.name;
  fileSizeEl.textContent = formatBytes(file.size);
  selectedFileEl.classList.add('visible');
  analyzeBtn.disabled = false;
}

function formatBytes(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// ─── Form Submission ──────────────────────────────────────
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!selectedFile) {
    showToast('📂 Please select a resume file first.');
    return;
  }

  const role = document.getElementById('targetRole').value;

  // Show progress
  analyzeBtn.disabled = true;
  analyzeBtn.querySelector('.btn-text').innerHTML = '<span>⏳</span> Analyzing...';
  progressEl.classList.add('visible');

  // Animate progress steps
  const stepMessages = [
    { pct: 20,  label: 'Parsing document...' },
    { pct: 45,  label: 'Scoring resume structure...' },
    { pct: 68,  label: 'Running ATS keyword check...' },
    { pct: 88,  label: 'Generating smart feedback...' },
    { pct: 100, label: 'Saving results...' },
  ];

  for (let i = 0; i < stepMessages.length; i++) {
    await delay(600);
    progressFill.style.width = stepMessages[i].pct + '%';
    document.getElementById(`step${i+1}`).classList.add('active');
    if (i > 0) document.getElementById(`step${i}`).classList.replace('active', 'done');
    document.getElementById(`step${i+1}-icon`).textContent = '↻';
  }

  // Send API request
  const formData = new FormData();
  formData.append('resume', selectedFile);
  formData.append('role', role);

  try {
    const resp = await fetch('/analyze', { method: 'POST', body: formData });
    const data = await resp.json();

    if (!resp.ok || data.error) {
      throw new Error(data.error || 'Analysis failed.');
    }

    // Mark all done
    for (let i = 1; i <= 5; i++) {
      const step = document.getElementById(`step${i}`);
      if (step) {
        step.classList.remove('active');
        step.classList.add('done');
        document.getElementById(`step${i}-icon`).textContent = '✓';
      }
    }

    // Store data and redirect
    sessionStorage.setItem('analysisData', JSON.stringify(data.dashboard_data));
    await delay(600);
    window.location.href = data.redirect_url;

  } catch (err) {
    showToast('❌ ' + err.message);
    progressEl.classList.remove('visible');
    analyzeBtn.disabled = false;
    analyzeBtn.querySelector('.btn-text').innerHTML = '<span>🚀</span> Analyze Resume';
    progressFill.style.width = '0%';
    progressSteps.forEach(s => s.classList.remove('active', 'done'));
  }
});

// ─── Toast Notification ───────────────────────────────────
function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 4000);
}

function delay(ms) { return new Promise(r => setTimeout(r, ms)); }
