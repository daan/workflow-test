from app import app
from livereload import Server

if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch("./templates/")
    server.watch("./style/")
    server.watch("../aframe/")
    server.watch("../threejs/")
    server.watch("../README.md")

    server.serve()
