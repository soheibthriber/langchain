from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()


def _html_page(inner: str) -> str:
    return f"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Lesson 1 Graph</title>
    <style>
      body {{ font-family: system-ui, sans-serif; margin: 24px; }}
      .container {{ max-width: 1100px; margin: 0 auto; }}
    </style>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
  </head>
  <body>
    <div class="container">
      <h1>Lesson 1 — Hello, Chain</h1>
      {inner}
      <p style="margin-top:16px;color:#666">Edit lessons/01_hello_chain/graph.mmd and refresh.</p>
    </div>
  </body>
  </html>
  """


@app.get("/", response_class=HTMLResponse)
def show_graph() -> HTMLResponse:
    root = Path(__file__).resolve().parents[1]
    mmd_path = root / "lessons/01_hello_chain/graph.mmd"
    if not mmd_path.exists():
        body = "<p>Run Lesson 1 first to generate <code>graph.mmd</code>:</p>" \
               "<pre>python3 lessons/01_hello_chain/code.py</pre>"
        return HTMLResponse(content=_html_page(body))
    mmd = mmd_path.read_text(encoding="utf-8")
    body = f"<div class=\"mermaid\">\n{mmd}\n</div>"
    return HTMLResponse(content=_html_page(body))
