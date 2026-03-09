from flask import Flask
import os

app = Flask(__name__)
# Es importante que estas variables de entorno se llamen igual que en el 'docker run'
student = os.getenv("STUDENT_NAME", "Kevin")
hood = os.getenv("BARRIO", "Villa Paulina")

@app.get("/")
def home():
    msg = f"Hola, soy {student} y vivo en {hood}"
    # La ruta debe coincidir con el punto de montaje del volumen
    with open("/var/log/app/visitas.log", "a") as f:
        f.write(msg + "\n")
    return msg

@app.get("/health")
def health():
    return {"ok": True}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)