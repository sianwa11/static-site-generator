
from enum import Enum
from parentnode import ParentNode
from leafnode import LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  OLIST = "ordered_list"
  ULIST = "unordered_list"


def markdown_to_blocks(markdown):
  result = []

  if markdown == "" or markdown == None:
    return result
  
  blocks = markdown.strip().split("\n\n")
  
  for block in blocks:
    if block == "":
      continue

    stripped = list(map(lambda str: str.strip(),block.strip().split("\n")))
 
    result.append("\n".join(stripped))
  
  return result


def block_to_block_type(block):
  lines = block.split("\n")

  if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
      return BlockType.HEADING
  if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
      return BlockType.CODE
  if block.startswith(">"):
      for line in lines:
          if not line.startswith(">"):
              return BlockType.PARAGRAPH
      return BlockType.QUOTE
  if block.startswith("- "):
      for line in lines:
          if not line.startswith("- "):
              return BlockType.PARAGRAPH
      return BlockType.ULIST
  if block.startswith("1. "):
      i = 1
      for line in lines:
          if not line.startswith(f"{i}. "):
              return BlockType.PARAGRAPH
          i += 1
      return BlockType.OLIST
  return BlockType.PARAGRAPH


def text_to_children(text):
   text_nodes = text_to_textnodes(text)
   children = []
   for text_node in text_nodes:
      html_node = text_node_to_html_node(text_node)
      children.append(html_node)
   return children

def olist_to_html_node(block):
   items = block.split("\n")
   html_items = []
   for item in items:
      text = item[3:]
      children = text_to_children(text)
      html_items.append(ParentNode("li", children))
   return ParentNode("ol", html_items)

def block_to_htmlnode(block):
   block_type = block_to_block_type(block)

   match (block_type):
      case BlockType.HEADING:
         text = block.split("#")
         tag = f"h{len(text)-1}"
         children = text_to_textnodes(text[1].strip())
         nodes = list(map(lambda text_node: text_node_to_html_node(text_node) ,children))

         return ParentNode(tag, nodes)

      case BlockType.CODE:
         code = block.split("```")
         return ParentNode("pre", [LeafNode("code", code[1])]) 

      case BlockType.QUOTE:
         quotes_arr = block.split(">")
         quotes = "".join(quotes_arr[1:]).strip()

         return LeafNode("blockquote", quotes)
      
      case BlockType.ULIST:
         items = block.split("\n")
         html_items = []
         for item in items:
            if item == "":
               continue
            text = item[2:]
            children = text_to_children(text)
            html_items.append(ParentNode("li", children))
         return ParentNode("ul", html_items)
         # list_arr = block.split("-")
         # nodes = []
         # for list_item in list_arr:
         #    if list_item == "":
         #       continue
         #    nodes.append(LeafNode("li", list_item))
         # return ParentNode("ul", nodes)
      
      case BlockType.OLIST:
         return olist_to_html_node(block)
         # list_arr = block.split("\n")
         # nodes = []
         # for i in range(len(list_arr)):
         #    item = list_arr[i].replace(f"{i+1}. ", "")
         #    # text_nodes = text_to_textnodes(item)
         #    # nodes.extend(list(map(lambda text_node: text_node_to_html_node(text_node) ,text_nodes)))

         #    nodes.append(LeafNode("li", item))
            
         # return ParentNode("ol", nodes)

      case _:
         text_nodes = text_to_textnodes(block)
         nodes = list(map(lambda text_node: text_node_to_html_node(text_node) ,text_nodes))
         return ParentNode("p", nodes)
   

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  nodes = [] 

  for block in blocks:
     nodes.append(block_to_htmlnode(block))
  
  parent_node = ParentNode("div", nodes)
  return parent_node

