from app import app
from flask_frozen import Freezer
from pathlib import Path


build_dir = Path("build/")

frameworks = [
    f.name
    for f in Path("..").iterdir()
    if f.is_dir() and f.name not in [".git", "web", ".vscode"]
]


print(frameworks)


# def copy_static_files():
#     for f in Path("..").iterdir():
#         if f.is_dir() and f.name not in [".git", "web", ".vscode"]:
#             # make folder
#             print(build_dir / f.name)


freezer = Freezer(app)

if __name__ == "__main__":
    freezer.freeze()
