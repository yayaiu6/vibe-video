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
  setupFileUpload();
  autoResizeTextarea();
  checkBackend();
}

async function checkBackend() {
  const ok = await Api.healthCheck();
  const badge = document.getElementById('backendStatus');
  if (badge) {
    badge.textContent = ok ? 'Connected' : 'Offline';
    badge.style.color = ok ? 'var(--success)' : 'var(--error)';
  }
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

function setupFileUpload() {
  document.querySelectorAll('.prompt-attachments button').forEach((btn, i) => {
    btn.addEventListener('click', () => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = i === 0 ? 'image/*' : i === 1 ? 'video/*' : '*';
      input.multiple = true;
      input.onchange = () => {
        const files = Array.from(input.files);
        if (!files.length) return;
        if (!AppStore.pendingFiles) AppStore.pendingFiles = [];
        AppStore.pendingFiles.push(...files);
        showAttachedFiles();
      };
      input.click();
    });
  });
}

function showAttachedFiles() {
  const container = document.querySelector('.prompt-attachments');
  if (!container) return;
  container.querySelectorAll('.attached-file').forEach(e => e.remove());
  (AppStore.pendingFiles || []).forEach((f, i) => {
    const tag = document.createElement('span');
    tag.className = 'attached-file';
    tag.innerHTML = `${f.name} <button onclick="removeFile(${i})">&times;</button>`;
    container.appendChild(tag);
  });
}

window.removeFile = function(idx) {
  AppStore.pendingFiles.splice(idx, 1);
  showAttachedFiles();
};

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

async function handleGenerate() {
  const input = document.getElementById('promptInput');
  const prompt = input.value.trim();
  if (!prompt || AppStore.isGenerating) return;

  AppStore.addMessage('user', prompt);
  renderMessages();
  input.value = '';
  autoResize(input);
  hideWelcome();

  const files = AppStore.pendingFiles || [];
  AppStore.pendingFiles = [];
  showAttachedFiles();

  showPipeline();

  let fullResponse = '';
  let runId = null;

  AppStore._stream = Api.streamTeam(prompt, {
    sessionId: AppStore.activeConversation?.sessionId || null,
    userId: 'frontend-user',
    files,
    onEvent(type, data) {
      updatePipelineStage(type, data);

      if (data?.content) {
        fullResponse += data.content;
        updateStreamingMessage(fullResponse);
      }
      if (data?.run_id) runId = data.run_id;
      if (data?.session_id) {
        if (!AppStore.activeConversation) {
          AppStore.addConversation({ id: Date.now(), title: prompt.slice(0, 40), messages: [], sessionId: data.session_id });
        } else {
          AppStore.activeConversation.sessionId = data.session_id;
        }
      }
      if (data?.content && type === 'TeamRunContent') {
        const status = document.getElementById('pipelineStatus');
        if (status) status.textContent = 'AI is generating...';
      }
    },
    onDone(type, data) {
      hidePipeline();
      AppStore.isGenerating = false;
      AppStore._stream = null;

      if (type === 'TeamRunError' || type === 'RunError') {
        const errMsg = data?.content || data?.error || 'Generation failed';
        addAiMessage('Error: ' + errMsg);
        return;
      }

      if (fullResponse) {
        finalizeMessage(fullResponse);
        extractVideoFromResponse(fullResponse);
      } else {
        addAiMessage('Generation completed but no response content received.');
      }
    },
    onError(err) {
      hidePipeline();
      AppStore.isGenerating = false;
      AppStore._stream = null;
      addAiMessage('Connection error: ' + err.message);
    },
  });
}

function addAiMessage(text) {
  AppStore.addMessage('ai', text);
  renderMessages();
}

function updateStreamingMessage(text) {
  const area = document.getElementById('chatArea');
  if (!area) return;

  let streamMsg = document.getElementById('streaming-msg');
  if (!streamMsg) {
    streamMsg = document.createElement('div');
    streamMsg.id = 'streaming-msg';
    streamMsg.className = 'chat-msg ai';
    streamMsg.innerHTML = `
      <div class="msg-avatar ai"><i data-lucide="sparkles" class="icon-sm"></i></div>
      <div class="msg-bubble ai"></div>
    `;
    area.appendChild(streamMsg);
    lucide.createIcons();
  }

  streamMsg.querySelector('.msg-bubble').innerHTML = formatMarkdown(text);
  area.scrollTop = area.scrollHeight;
}

function finalizeMessage(text) {
  const streamMsg = document.getElementById('streaming-msg');
  if (streamMsg) streamMsg.remove();

  AppStore.addMessage('ai', text);
  renderMessages();
}

function extractVideoFromResponse(text) {
  const videoMatch = text.match(/(?:\/renders\/|\.\/renders\/)[^\s)"]+\.mp4/i);
  if (videoMatch) {
    const videoPath = videoMatch[0];
    showVideoResult(videoPath);
  }
}

function showVideoResult(videoPath) {
  const placeholder = document.getElementById('videoPlaceholder');
  const controls = document.getElementById('videoControls');
  if (!placeholder) return;

  const filename = videoPath.split('/').pop();
  const downloadUrl = Api.baseUrl + '/renders/' + filename;

  placeholder.innerHTML = `
    <video controls style="width:100%;height:100%;object-fit:contain;border-radius:var(--radius-md)">
      <source src="${downloadUrl}" type="video/mp4">
      Your browser does not support video.
    </video>
  `;
  if (controls) controls.style.display = 'flex';
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
      <div class="msg-bubble ${msg.role}">${formatMarkdown(msg.content)}</div>
    </div>
  `).join('');
  lucide.createIcons();
  area.scrollTop = area.scrollHeight;
}

function formatMarkdown(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>');
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
}

function resetPipeline() {
  document.querySelectorAll('.p-step').forEach(s => { s.classList.remove('active', 'done'); });
  const bar = document.getElementById('pipelineBar');
  if (bar) bar.style.width = '0%';
  const status = document.getElementById('pipelineStatus');
  if (status) status.textContent = 'Initializing...';
}

function updatePipelineStage(type, data) {
  const stageMap = {
    'RunStarted': 0,
    'TeamRunStarted': 0,
    'AgentRunStarted': 1,
    'ToolCallStarted': 2,
    'ToolCallCompleted': 3,
    'Thinking': 1,
    'Content': 4,
    'RunCompleted': 6,
    'TeamRunCompleted': 6,
  };

  const idx = stageMap[type] ?? -1;
  if (idx < 0) return;

  const stages = document.querySelectorAll('.p-step');
  stages.forEach((s, i) => {
    s.classList.remove('active', 'done');
    if (i < idx) s.classList.add('done');
    else if (i === idx) s.classList.add('active');
  });

  const bar = document.getElementById('pipelineBar');
  if (bar) bar.style.width = ((idx + 1) / 7 * 100) + '%';

  const status = document.getElementById('pipelineStatus');
  const labels = {
    'RunStarted': 'Starting team...',
    'TeamRunStarted': 'Team coordinating...',
    'AgentRunStarted': 'Agent working...',
    'ToolCallStarted': 'Using tools...',
    'ToolCallCompleted': 'Tool complete',
    'Thinking': 'Thinking...',
    'Content': 'Generating response...',
    'RunCompleted': 'Complete!',
    'TeamRunCompleted': 'Complete!',
  };
  if (status) status.textContent = labels[type] || type;
}

function hidePipeline() {
  const overlay = document.getElementById('pipelineOverlay');
  if (overlay) overlay.style.display = 'none';
}

window.cancelGeneration = function() {
  if (AppStore._stream) {
    AppStore._stream.abort();
    AppStore._stream = null;
  }
  AppStore.isGenerating = false;
  hidePipeline();
  addAiMessage('Generation cancelled.');
};
