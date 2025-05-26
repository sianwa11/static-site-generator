import re
import os

from block_markdown import markdown_to_html_node

def extract_title(markdown):
  pattern = r"^#\s+(.+)$"
  heading = re.search(pattern, markdown, re.MULTILINE)
  if not heading:
    raise Exception("A title is required")
  
  return heading.group(1)

def generate_page(from_path, template_path, dest_path, basepath=None):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")

  md = read_and_store(from_path)
  template = read_and_store(template_path)

  html = markdown_to_html_node(md).to_html()
  title = extract_title(md)

  result = template.replace("{{ Title }}", title).replace("{{ Content }}", html).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
  
  try:
    html_file = open(dest_path, "w")
    html_file.writelines(result)
    html_file.close()
  except:
    raise Exception(f"Something went wrong writing to {dest_path}")
 
def read_and_store(path):
  try:
    content = open(path, 'r')
    lines = content.readlines()
    result = ""

    for line in lines:
      result += line
    return result
  except:
    raise Exception(f"File {path} not found")


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath=None):
  if not os.path.exists(dir_path_content):
    raise Exception(f"{dir_path_content} does not exist")
  
  for filename in os.listdir(dir_path_content):
    filepath = os.path.join(dir_path_content, filename)
    if os.path.isfile(filepath):
      print(f"writing to {dest_dir_path}/index.html")
      content = f"{dir_path_content}/index.md"
      dest = f"{dest_dir_path}/index.html"
      generate_page(content, template_path, dest, basepath)
    else:
      print(f"recurse...{filename}")
      directory = f"{dest_dir_path}/{filename}"
      if not os.path.exists(directory):
        os.mkdir(directory)
        print(f"Made directory: {directory}")
      generate_page_recursive(filepath, template_path, directory, basepath)

  pass


# generate_page("./content/index.md", "./template.html", "./index.html")