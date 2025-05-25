import re

from block_markdown import markdown_to_html_node

def extract_title(markdown):
  pattern = r"^#\s+(.+)$"
  heading = re.search(pattern, markdown, re.MULTILINE)
  if not heading:
    raise Exception("A title is required")
  
  return heading.group(1)

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")

  md = read_and_store(from_path)
  template = read_and_store(template_path)

  html = markdown_to_html_node(md).to_html()
  title = extract_title(md)

  result = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
  
  try:
    html_file = open(dest_path, "w")
    html_file.writelines(result)
    html_file.close()
  except:
    raise Exception(f"Something went wrong writing to {dest_path}")
 
  pass

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



# generate_page("./content/index.md", "./template.html", "./index.html")