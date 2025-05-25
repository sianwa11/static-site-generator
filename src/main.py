from copystatic import copy_dir
from generatepage import generate_page


def main():
    copy_dir("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

    pass

   

main()