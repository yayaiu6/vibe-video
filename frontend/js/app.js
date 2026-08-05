document.addEventListener('DOMContentLoaded', () => {
  lucide.createIcons();
  initApp();
});

function initApp() {
  setupPromptDock();
  setupQuickPrompts();
  setupPresets();
  setupConversationList();
  setupSettingsBindings();
  autoResizeTextarea();
}

function setupPromptDock() {
  const input = document.getElementById('promptInput');
  const btn = document.getElementById('generateBtn');
  if (!input || !btn) return;

  btn.addEventListener('click', () => handleGenerate());

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleGenerate();
    }
  });
}

function setupQuickPrompts() {
  document.querySelectorAll('.quick-prompt').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = document.getElementById('promptInput');
      input.value = btn.dataset.prompt;
      input.focus();
      autoResize(input);
    });
  });
}

function setupPresets() {
  document.querySelectorAll('.preset-chip').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.preset-chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      AppStore.updateSettings({ style: btn.textContent.trim().toLowerCase() });
    });
  });
}

function setupConversationList() {
  document.querySelectorAll('.conv-item').forEach(item => {
    item.addEventListener('click', () => {
      document.querySelectorAll('.conv-item').forEach(i => i.classList.remove('active'));
      item.classList.add('active');
    });
  });
}

function setupSettingsBindings() {
  document.querySelectorAll('.panel-right select').forEach(sel => {
    sel.addEventListener('change', () => {
      const key = sel.previousElementSibling?.textContent?.trim();
      const map = { 'Duration': 'duration', 'Resolution': 'resolution', 'FPS': 'fps', 'Aspect Ratio': 'aspectRatio', 'Style': 'style' };
      if (map[key]) AppStore.updateSettings({ [map[key]]: sel.value });
    });
  });

  const seedInput = document.querySelector('.panel-right input[type="number"]');
  if (seedInput) seedInput.addEventListener('change', () => AppStore.updateSettings({ seed: seedInput.value || null }));

  const strictCheck = document.getElementById('strictMode');
  if (strictCheck) strictCheck.addEventListener('change', () => AppStore.updateSettings({ strictMode: strictCheck.checked }));
}

function autoResizeTextarea() {
  const ta = document.getElementById('promptInput');
  if (!ta) return;
  ta.addEventListener('input', () => autoResize(ta));
}

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function handleGenerate() {
  const input = document.getElementById('promptInput');
  const prompt = input.value.trim();
  if (!prompt || AppStore.isGenerating) return;

  AppStore.addMessage('user', prompt);
  renderMessages();
  input.value = '';
  autoResize(input);

  hideWelcome();
  showPipeline();
  simulateGeneration(prompt);
}

function renderMessages() {
  const area = document.getElementById('chatArea');
  if (!area) return;
  const messages = AppStore.getActiveMessages();
  area.innerHTML = messages.map(msg => `
    <div class="chat-msg ${msg.role}">
      <div class="msg-avatar ${msg.role}">
        <i data-lucide="${msg.role === 'user' ? 'user' : 'sparkles'}" class="icon-sm"></i>
      </div>
      <div class="msg-bubble ${msg.role}">${escapeHtml(msg.content)}</div>
    </div>
  `).join('');
  lucide.createIcons();
  area.scrollTop = area.scrollHeight;
}

function hideWelcome() {
  const w = document.getElementById('chatWelcome');
  if (w) w.style.display = 'none';
}

function showPipeline() {
  AppStore.isGenerating = true;
  const overlay = document.getElementById('pipelineOverlay');
  if (overlay) overlay.style.display = 'flex';
  resetPipeline();
  animatePipeline();
}

function resetPipeline() {
  document.querySelectorAll('.p-step').forEach(s => { s.classList.remove('active', 'done'); });
  const bar = document.getElementById('pipelineBar');
  if (bar) bar.style.width = '0%';
  const status = document.getElementById('pipelineStatus');
  if (status) status.textContent = 'Initializing...';
}

function animatePipeline() {
  const stages = ['parse', 'style', 'script', 'frames', 'animate', 'render', 'done'];
  const labels = ['Parsing prompt...', 'Applying style...', 'Generating script...', 'Creating frames...', 'Animating...', 'Rendering MP4...', 'Complete!'];
  let i = 0;

  const interval = setInterval(() => {
    if (i >= stages.length) {
      clearInterval(interval);
      setTimeout(() => completeGeneration(), 500);
      return;
    }

    if (i > 0) {
      const prev = document.querySelector(`.p-step[data-stage="${stages[i-1]}"]`);
      if (prev) { prev.classList.remove('active'); prev.classList.add('done'); }
    }

    const curr = document.querySelector(`.p-step[data-stage="${stages[i]}"]`);
    if (curr) curr.classList.add('active');

    const bar = document.getElementById('pipelineBar');
    if (bar) bar.style.width = ((i + 1) / stages.length * 100) + '%';

    const status = document.getElementById('pipelineStatus');
    if (status) status.textContent = labels[i];

    i++;
  }, 800);
}

async function completeGeneration() {
  const overlay = document.getElementById('pipelineOverlay');
  if (overlay) overlay.style.display = 'none';
  AppStore.isGenerating = false;

  AppStore.addMessage('ai', 'Here\'s your generated video! You can download it, share the link, or edit the prompt to regenerate.');
  renderMessages();

  const placeholder = document.getElementById('videoPlaceholder');
  const controls = document.getElementById('videoControls');
  if (placeholder) placeholder.innerHTML = '<div style="text-align:center;color:var(--text-muted)"><i data-lucide="check-circle" style="width:48px;height:48px;margin-bottom:8px;color:var(--success)"></i><p>Video generated successfully!</p></div>';
  if (controls) controls.style.display = 'flex';
  lucide.createIcons();
}

function escapeHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

async function simulateGeneration(prompt) {
  try {
    await Api.healthCheck();
    AppStore.addMessage('ai', `I'll create a video based on your prompt: "${prompt}". Processing through the generation pipeline now...`);
    renderMessages();
  } catch {
    AppStore.addMessage('ai', 'Backend not connected. This is a frontend demo — the video will appear after generation completes.');
    renderMessages();
  }
}
