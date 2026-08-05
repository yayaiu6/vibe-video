const Api = {
  baseUrl: AppStore.backendUrl,

  async healthCheck() {
    try {
      const res = await fetch(`${this.baseUrl}/health`);
      return res.ok;
    } catch { return false; }
  },

  async sendMessage(prompt, files = []) {
    const formData = new FormData();
    formData.append('message', prompt);
    files.forEach((f, i) => formData.append(`file_${i}`, f));

    const res = await fetch(`${this.baseUrl}/run`, {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  },

  async sendChat(message, conversationId = null) {
    const body = { message };
    if (conversationId) body.conversation_id = conversationId;

    const res = await fetch(`${this.baseUrl}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  },
};
