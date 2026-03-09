import os
import pathlib
import datetime
from fastapi import FastAPI, Request, Response

app = FastAPI()

# Environment variables
STUDENT = os.getenv("STUDENT_NAME", "Anon")
BARRIO = os.getenv("BARRIO", "barrio-desconocido")
LOG_PATH = "/var/log/app/visitas.log"

# Ensure log directory exists
pathlib.Path("/var/log/app").mkdir(parents=True, exist_ok=True)

def log_visit(request: Request, msg: str):
    """Logs the timestamp, client IP, and message to a file."""
    # Use timezone-aware UTC
    ts = datetime.datetime.now(datetime.UTC).isoformat()
    client_ip = request.client.host if request.client else "unknown"
    line = f"{ts} ip={client_ip} path={request.url.path} msg={msg}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)

@app.get("/")
async def root(request: Request):
    """Main entry point returning plain text."""
    msg = f"Hola, soy {STUDENT} y vivo en {BARRIO}"
    log_visit(request, msg)
    return Response(content=msg, media_type="text/plain; charset=utf-8")

@app.get("/health")
async def health():
    """Health check endpoint for monitoring."""
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)