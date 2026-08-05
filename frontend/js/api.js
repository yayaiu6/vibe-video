const Api = {
  baseUrl: window.location.origin,

  async healthCheck() {
    try {
      const res = await fetch(`${this.baseUrl}/health`);
      return res.ok;
    } catch { return false; }
  },

  async runTeam(prompt, { sessionId, userId, files, stream = true } = {}) {
    const formData = new FormData();
    formData.append('message', prompt);
    formData.append('stream', stream);
    formData.append('monitor', 'true');
    if (sessionId) formData.append('session_id', sessionId);
    if (userId) formData.append('user_id', userId);
    if (files && files.length) {
      files.forEach(f => formData.append('files', f));
    }

    const res = await fetch(`${this.baseUrl}/teams/vibe_video/runs`, {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`API error ${res.status}: ${err}`);
    }

    return res;
  },

  async runTeamJson(prompt, opts = {}) {
    const res = await this.runTeam(prompt, { ...opts, stream: false });
    return res.json();
  },

  streamTeam(prompt, { sessionId, userId, files, onEvent, onDone, onError } = {}) {
    const controller = new AbortController();

    this.runTeam(prompt, { sessionId, userId, files, stream: true })
      .then(async res => {
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop();

          for (const line of lines) {
            if (line.startsWith('event: ')) {
              var eventType = line.slice(7).trim();
            } else if (line.startsWith('data: ') && eventType) {
              try {
                const data = JSON.parse(line.slice(6));
                onEvent?.(eventType, data);
                if (eventType === 'RunCompleted' || eventType === 'RunError') {
                  onDone?.(eventType, data);
                  return;
                }
              } catch {}
              eventType = null;
            }
          }
        }
        onDone?.('StreamEnd', null);
      })
      .catch(err => onError?.(err));

    return { abort: () => controller.abort() };
  },

  async getTeamRuns() {
    const res = await fetch(`${this.baseUrl}/teams/vibe_video/runs?limit=20`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  },

  async getRun(teamId, runId) {
    const res = await fetch(`${this.baseUrl}/teams/${teamId}/runs/${runId}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  },
};
