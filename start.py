import os
import sys
from flask import Flask, send_from_directory, request
from flask_sock import Sock

# Adiciona o diretório raiz ao sys.path
ENABLE_CACHE = False
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.main import register_routes

app = Flask(__name__, static_folder="frontend", static_url_path="")
sock = Sock(app)

register_routes(app, sock)


@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


@app.after_request
def manage_cache(response):
    path = request.path

    if ENABLE_CACHE:
        # --- COMPORTAMENTO COM CACHE ATIVADO ---
        # CSS, JS e imagens ficam salvos por 1 ano
        if path.endswith(
            (
                ".css",
                ".js",
                ".png",
                ".jpg",
                ".jpeg",
                ".svg",
                ".gif",
                ".ico",
                ".woff",
                ".woff2",
                ".webp",
            )
        ):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        # HTML e rotas principais exigem validação constante
        elif path.endswith(".html") or path == "/" or not "." in path.split("/")[-1]:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    else:
        # --- COMPORTAMENTO COM CACHE DESATIVADO ---
        # Nenhum arquivo fica em cache (tudo é recarregado a cada F5)
        response.headers["Cache-Control"] = (
            "no-cache, no-store, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
