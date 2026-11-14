import os
import importlib


def register_routes(app, sock=None):
    routes_dir = os.path.join(os.path.dirname(__file__), "routes")
    print(routes_dir)
    for file in os.listdir(routes_dir):
        if not file.endswith(".py"):
            continue

        if file == "__init__.py":
            continue

        module = importlib.import_module(f"backend.routes.{file[:-3]}")

        if hasattr(module, "register"):
            try:
                module.register(app, sock)
            except TypeError:
                module.register(app)
