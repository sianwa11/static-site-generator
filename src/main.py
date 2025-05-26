from copystatic import copy_dir
from generatepage import generate_page, generate_page_recursive


def main():
    copy_dir("./static", "./public")
    # generate_page("./content/index.md", "./template.html", "./public/index.html")

    generate_page_recursive("./content", "./template.html", "./public")

    pass

   

main()