
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


def block_to_htmlnode(block):
   block_type = block_to_block_type(block)

   match (block_type):
      case BlockType.HEADING:
         text = block.split("#")
         tag = f"h{len(text)-1}"
         children = text_to_textnodes(text[1])
         nodes = list(map(lambda text_node: text_node_to_html_node(text_node) ,children))

         return ParentNode(tag, nodes)

      case BlockType.CODE:
         code = block.split("```")
         return ParentNode("pre", [LeafNode("code", code[1])]) 

      case BlockType.QUOTE:
         quotes_arr = block.split(">")
         quotes = "".join(quotes_arr[1:])

         return LeafNode("blockquote", quotes)
      
      case BlockType.ULIST:
         list_arr = block.split("-")
         nodes = []
         for list_item in list_arr:
            if list_item == "":
               continue
            nodes.append(LeafNode("li", list_item))
                 
         return ParentNode("ul", nodes)
      
      case BlockType.OLIST:
         list_arr = block.split("\n")
         nodes = []
         for list_item in list_arr:
            nodes.append(LeafNode("li", list_item))
            
         return ParentNode("ol", nodes)

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

