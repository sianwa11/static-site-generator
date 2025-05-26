import sys
from pathlib import Path

from copystatic import copy_dir
from generatepage import generate_page, generate_page_recursive


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    root = Path(__file__).resolve().parent.parent


    # copy_dir("/static", "/public")
    # generate_page("./content/index.md", "./template.html", "./public/index.html")
    # generate_page_recursive("/content", "/template.html", "/public")

    # copy_dir(f"{basepath}static", f"{basepath}docs")

    # generate_page_recursive(f"{basepath}content", f"{basepath}template.html", f"{basepath}docs", basepath)

    copy_dir(root / "static", root / "docs")
    generate_page_recursive(root / "content", root / "template.html", root / "docs", basepath)

    pass

   

main()