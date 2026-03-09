import os
import pathlib
import datetime
from fastapi import FastAPI, Request, Response

app = FastAPI()

STUDENT = os.getenv("STUDENT_NAME", "David Carvajal")
BARRIO = os.getenv("BARRIO", "Manuela Beltran")
LOG_PATH = "/var/log/app/visitas.log"

pathlib.Path("/var/log/app").mkdir(parents=True, exist_ok=True)

def log_visit(request: Request, msg: str):
    ts = datetime.datetime.now(datetime.UTC).isoformat()
    client_ip = request.client.host if request.client else "unknown"
    line = f"{ts} ip={client_ip} msg={msg}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)

@app.get("/")
async def root(request: Request):
    msg = f"Hola, soy {STUDENT} y vivo en {BARRIO}"
    log_visit(request, msg)
    return Response(content=msg, media_type="text/plain")

@app.get("/health")
async def health():
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)