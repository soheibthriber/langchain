from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(title="LangChain Visualizer API")

# Enable CORS for the React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT = Path(__file__).resolve().parents[1]


@app.get("/")
def read_root():
    return {"message": "LangChain Visualizer API", "version": "1.1"}


@app.get("/api/runs/{lesson_id}/latest")
def get_latest_run(lesson_id: str):
    """Get the latest run for a lesson"""
    graph_path = ROOT / "lessons" / lesson_id / "graph.json"
    
    if not graph_path.exists():
        raise HTTPException(status_code=404, detail=f"No graph found for lesson {lesson_id}")
    
    try:
        with open(graph_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading graph: {str(e)}")


@app.get("/api/runs/{run_id}")
def get_run_by_id(run_id: str):
    """Get a specific run by ID (for future use when we store multiple runs)"""
    # For now, search through all lesson directories
    for lesson_dir in (ROOT / "lessons").iterdir():
        if lesson_dir.is_dir():
            graph_path = lesson_dir / "graph.json"
            if graph_path.exists():
                try:
                    with open(graph_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    if data.get('metadata', {}).get('run_id') == run_id:
                        return JSONResponse(content=data)
                except Exception:
                    continue
    
    raise HTTPException(status_code=404, detail=f"Run {run_id} not found")


@app.get("/api/lessons")
def list_lessons():
    """List available lessons"""
    lessons = []
    lessons_dir = ROOT / "lessons"
    
    if lessons_dir.exists():
        for lesson_dir in lessons_dir.iterdir():
            if lesson_dir.is_dir():
                graph_path = lesson_dir / "graph.json"
                if graph_path.exists():
                    try:
                        with open(graph_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        lessons.append({
                            "id": lesson_dir.name,
                            "lesson_id": data.get('metadata', {}).get('lesson_id'),
                            "run_id": data.get('metadata', {}).get('run_id'),
                            "created_at": data.get('metadata', {}).get('created_at'),
                            "latency_ms": data.get('run', {}).get('latency_ms'),
                            "events_count": len(data.get('events', []))
                        })
                    except Exception:
                        pass
    
    return {"lessons": lessons}


@app.get("/api/mermaid/{lesson_id}")
def get_mermaid(lesson_id: str):
    """Get Mermaid diagram for a lesson"""
    mermaid_path = ROOT / "lessons" / lesson_id / "graph.mmd"
    
    if not mermaid_path.exists():
        raise HTTPException(status_code=404, detail=f"No Mermaid diagram found for lesson {lesson_id}")
    
    try:
        content = mermaid_path.read_text(encoding='utf-8')
        return {"mermaid": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading Mermaid: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
