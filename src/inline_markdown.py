import re
from textnode import *

def extract_markdown_images(text):
  # return re.findall(r"\w+ !\[(\w+)\]\((.*?)\)", text)
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
  new_nodes = []
  for old_node in old_nodes:
      if old_node.text_type != TextType.TEXT:
          new_nodes.append(old_node)
          continue
      original_text = old_node.text
      img_data = extract_markdown_images(original_text)
      
      if len(img_data) == 0:
          new_nodes.append(TextNode(original_text, TextType.TEXT))
          continue

      last_index = 0
      for alt_text, src in img_data:
          markdown_img = f"![{alt_text}]({src})"
          index = original_text.find(markdown_img, last_index)
          
          if index > last_index:
              new_nodes.append(TextNode(original_text[last_index:index], TextType.TEXT))
          new_nodes.append(TextNode(alt_text, TextType.IMAGE, src))

          last_index = index + len(markdown_img)

      if last_index < len(original_text):
          new_nodes.append(TextNode(original_text[last_index:], TextType.TEXT))
  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []

  for old_node in old_nodes:
      if old_node.text_type != TextType.TEXT:
          new_nodes.append(old_node)
          continue
      original_text = old_node.text
      links = extract_markdown_links(original_text)

      if len(links) == 0:
          new_nodes.append(TextNode(original_text, TextType.TEXT))
          continue
      
      last_index = 0
      for link_alt, link in links:
          markdown_link = f"[{link_alt}]({link})"
          text = old_node.text
          index = text.find(markdown_link, last_index)
          
          if index > last_index:
              new_nodes.append(TextNode(text[last_index:index], TextType.TEXT))
          
          new_nodes.append(TextNode(link_alt, TextType.LINK, link))
          last_index = index + len(markdown_link)

      if last_index < len(original_text):
          new_nodes.append(TextNode(original_text[last_index:], TextType.TEXT))
  return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for old_node in old_nodes:
      if old_node.text_type != TextType.TEXT:
          new_nodes.append(old_node)
          continue

      splitted = old_node.text.split(delimiter)

      if len(splitted) % 2 == 0:
          raise Exception("Invalid markdown syntax")
      split_nodes = []
      for i in range(len(splitted)):
          if splitted[i] == "":
              continue
          if i % 2 == 0:
              split_nodes.append(TextNode(splitted[i], TextType.TEXT))
          else:
              split_nodes.append(TextNode(splitted[i], text_type))
      new_nodes.extend(split_nodes)
  return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes