/**
 * ModelArena — VS Code Extension
 * Right-click selected text → "Evaluate with ModelArena"
 * Results appear in a dedicated Webview panel.
 */
const vscode = require("vscode");
const https  = require("https");

const API_BASE = "http://localhost:8000"; // configurable in settings

function activate(context) {
  // ── Command: evaluate selected text ──────────────────────────────
  const evalCmd = vscode.commands.registerCommand(
    "modelarena.evaluate",
    async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) return;

      const selection = editor.document.getText(editor.selection);
      if (!selection.trim()) {
        vscode.window.showWarningMessage("Select some text first to evaluate.");
        return;
      }

      // Show panel immediately with loading state
      const panel = vscode.window.createWebviewPanel(
        "modelarena",
        "ModelArena — Evaluating…",
        vscode.ViewColumn.Beside,
        { enableScripts: true }
      );
      panel.webview.html = loadingHtml(selection);

      // Call backend
      try {
        const result = await callEvalAPI(selection);
        panel.title = "ModelArena — Results";
        panel.webview.html = resultsHtml(selection, result);
      } catch (err) {
        panel.webview.html = errorHtml(err.message);
      }
    }
  );

  context.subscriptions.push(evalCmd);
}

// ── API call ─────────────────────────────────────────────────────────
function callEvalAPI(prompt) {
  const config = vscode.workspace.getConfiguration("modelarena");
  const models  = config.get("models", ["claude-haiku-5-5", "gpt-4o-mini"]);
  const apiKey  = config.get("anthropicApiKey", "");

  const body = JSON.stringify({
    prompt,
    models,
    criteria: ["Accuracy", "Clarity", "Depth"],
    api_keys: { anthropic: apiKey },
  });

  return new Promise((resolve, reject) => {
    const req = https.request(`${API_BASE}/evaluate/`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(body) },
    }, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => resolve(JSON.parse(data)));
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

// ── HTML templates ────────────────────────────────────────────────────
function loadingHtml(prompt) {
  return `<!DOCTYPE html><html><body style="font-family:sans-serif;padding:20px;background:#0d1117;color:#e6edf3">
    <h2>⏳ Evaluating…</h2>
    <p style="color:#8b949e">${escHtml(prompt.slice(0, 120))}…</p>
  </body></html>`;
}

function resultsHtml(prompt, data) {
  const rows = (data.evaluations || [])
    .sort((a, b) => b.overall - a.overall)
    .map((ev, i) => {
      const crown = i === 0 ? "🥇" : i === 1 ? "🥈" : "🥉";
      return `<tr>
        <td>${crown} <strong>${ev.model_id}</strong></td>
        <td style="color:#58a6ff;font-size:18px">${ev.overall}/10</td>
        <td style="color:#8b949e">${ev.verdict || ""}</td>
      </tr>`;
    }).join("");

  return `<!DOCTYPE html><html><body style="font-family:sans-serif;padding:24px;background:#0d1117;color:#e6edf3">
    <h2 style="color:#58a6ff">🏆 ModelArena Results</h2>
    <p style="color:#8b949e;margin-bottom:16px"><em>${escHtml(prompt.slice(0, 200))}</em></p>
    <table style="width:100%;border-collapse:collapse">
      <thead><tr style="color:#6e7681;font-size:11px">
        <th style="text-align:left;padding:6px 0">Model</th>
        <th style="text-align:left;padding:6px 0">Score</th>
        <th style="text-align:left;padding:6px 0">Verdict</th>
      </tr></thead>
      <tbody>${rows}</tbody>
    </table>
    <p style="margin-top:20px;color:#8b949e;font-size:12px">💡 ${escHtml(data.comparison || "")}</p>
  </body></html>`;
}

function errorHtml(msg) {
  return `<!DOCTYPE html><html><body style="font-family:sans-serif;padding:20px;background:#0d1117;color:#f85149">
    <h2>Error</h2><p>${escHtml(msg)}</p>
    <p style="color:#8b949e">Make sure the ModelArena backend is running on port 8000.</p>
  </body></html>`;
}

function escHtml(str) {
  return String(str).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function deactivate() {}
module.exports = { activate, deactivate };
