const AppStore = {
  conversations: [],
  activeConversation: null,
  pendingFiles: [],
  settings: {
    model: 'gemini-3.5-flash-lite',
    duration: 5,
    resolution: '720p',
    fps: 24,
    aspectRatio: '16:9',
    style: 'cinematic',
    seed: null,
    strictMode: false,
  },
  backendUrl: 'https://abundant-analysis-production-8345.up.railway.app',
  isGenerating: false,

  set(key, value) { this[key] = value; },

  updateSettings(partial) { Object.assign(this.settings, partial); },

  addConversation(conv) {
    this.conversations.unshift(conv);
    this.activeConversation = conv;
    return conv;
  },

  addMessage(role, content) {
    if (!this.activeConversation) {
      this.addConversation({ id: Date.now(), title: content.slice(0, 40), messages: [] });
    }
    const msg = { id: Date.now(), role, content, timestamp: new Date() };
    this.activeConversation.messages.push(msg);
    return msg;
  },

  getActiveMessages() {
    return this.activeConversation ? this.activeConversation.messages : [];
  },
};
