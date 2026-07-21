CSS = """
:root {
  --brand-yellow: #ffd600;
  --brand-green: #125430;
  --brand-red: #e11a2c;
  --bg: #f5f7fb;
  --surface: #ffffff;
  --text: #202124;
  --muted: #5f6368;
  --border: #e4e7ec;
  --radius: 12px;
  --shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}

html, body {
  color-scheme: light !important;
  width: 1200px;
  justify-self: center;
}

body, .gradio-container, .gradio-container .wrap {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: -apple-system, "Segoe UI", Roboto, sans-serif !important;
}

#app-title {
  margin-bottom: 0.75rem !important;
}

#app-title .app-header {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.75rem !important;
  margin: 0 !important;
}

#app-title .brand-mark {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.3rem !important;
  padding: 0.25rem 0.45rem !important;
  border: 1px solid var(--border) !important;
  border-radius: 999px !important;
  background: var(--surface) !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
  line-height: 0 !important;
}

#app-title .brand-dot {
  display: block !important;
  width: 1rem !important;
  height: 1rem !important;
  min-width: 0.8rem !important;
  min-height: 0.8rem !important;
  aspect-ratio: 1 / 1 !important;
  border-radius: 50% !important;
  margin: 0 !important;
  padding: 0 !important;
  flex-shrink: 0 !important;
}

#app-title .brand-green { background: var(--brand-green) !important; }
#app-title .brand-yellow { background: var(--brand-yellow) !important; }
#app-title .brand-red { background: var(--brand-red) !important; }

#app-title .app-title-text {
  font-size: 1.2rem !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em !important;
  color: var(--brand-green) !important;
  line-height: 1.2 !important;
  white-space: nowrap !important;
}

#warning {
  margin-top: 0 !important;
}

#warning p, #warning b{
  color: var(--text) !important;
}

#results-box {
  background: var(--surface) !important;
  color: #000000 !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 1rem !important;
  overflow: auto !important;
  box-shadow: none !important;
  max-height: 420px !important;
}

#results-box *,
#results-box .prose *,
#results-box .markdown * {
  color: #000000 !important;
}

#results-box .scroll-fade {
  display: none !important;
}

#region-wrapper {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  box-shadow: var(--shadow) !important;
  padding: 0.85rem 1rem !important;
  
}

#region-dropdown label,
.gradio-dropdown label {
  color: var(--text) !important;
  font-weight: 600 !important;
}

#region-wrapper .styler,
#region-wrapper .full,
#region-dropdown,
.gradio-dropdown .search {
  background: var(--surface) !important;
  background-color: var(--surface) !important;
  color: var(--text) !important;
  background-image: none !important;
  box-shadow: none !important;
}

#region-dropdown input, span,
.gradio-dropdown input {
  background: transparent !important;
  background-color: transparent !important;
  color: var(--text) !important;
  padding: 8px 12px !important;
  box-shadow: none !important;
  -webkit-box-shadow: none !important;
}

#submit-btn,
.gradio-button button {
  background: var(--brand-green) !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: var(--radius) !important;
  font-weight: 600 !important;
  box-shadow: none !important;
  margin: 10px !important;
}

#submit-btn:hover,
.gradio-button button:hover {
  background: green !important;
  color: #ffffff !important;
}"""
