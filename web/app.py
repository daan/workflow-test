from flask import Flask, send_from_directory, render_template, abort
from pathlib import Path, PurePath
from markdown_it import MarkdownIt
from livereload import Server

md = MarkdownIt("commonmark", {"breaks": True, "html": True})


def title_abstract(path):
    content = md.render(path.read_text())
    title = content.split("\n")[0][4:-5]  # strip <h1> and </h1>
    abstract = content.split("\n")[1][3:-4]  # strip <p> and </p>
    return [title, abstract]


# print(title_abstract(Path("../aframe/project-1/README.md")))

examples = {
    f.name: {
        e.name: title_abstract(e / "README.md")[0]
        for e in Path("../" + f.name).iterdir()
        if (e.is_dir())
    }
    for f in Path("../").iterdir()
    if (f.is_dir() and f.name not in [".git", "web", ".vscode"])
}

config = {"title": "notes on webxr", "examples": examples}


def render(template, path, vars={}):
    with open(path, "r", encoding="utf-8") as file:
        return render_template(
            template, **config, **vars, content=md.render(file.read())
        )
    abort(404)


app = Flask(__name__, static_url_path="")
app.debug = True
# static file serving


@app.route("/style/<path:path>")
def send_style(path):
    return send_from_directory(Path("style"), path)


@app.route("/favicon.ico")
def send_favicon():
    return send_from_directory(Path("style"), "favicon.ico")


# build pages


@app.route("/<string:framework>/")
def framework_page(framework=None):
    if framework in examples.keys():
        return render(
            f"{framework}.html",
            Path("..") / Path(framework) / Path("README.md"),
            vars={"framework": framework, "example": None},
        )
    abort(404)


@app.route("/<string:framework>/<string:example>.html")
def framework_example_page(framework=None, example=None):
    if framework in examples.keys():
        if example in examples[framework]:
            return render(
                "example.html",
                Path("..") / Path(framework) / Path(example) / Path("README.md"),
                vars={"framework": framework, "example": example},
            )
    abort(404)


@app.route("/<string:framework>/<string:example>/<path:path>")
def framework_example_static_files(framework=None, example=None, path=None):
    if framework in examples.keys():
        if example in examples[framework]:
            return send_from_directory(
                Path("..") / Path(framework) / Path(example), path
            )
    abort(404)


# home page


@app.route("/")
def home_page():
    return render("index.html", Path("..") / Path("README.md"))


# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument("action")
#     args = parser.parse_args()
#     if args.action == "freeze":
#         from flask_frozen import Freezer

#         freezer = Freezer(app)
#         freezer.freeze()
#     elif args.action == "serve":
#         # app.run(debug=True, port=5000)
#         server = Server(app.wsgi_app)
#         server.serve()
