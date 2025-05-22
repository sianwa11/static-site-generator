from enum import Enum
from leafnode import LeafNode



class TextType(Enum):
  TEXT = "text"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINK = "link"
  IMAGE = "image"

class TextNode():
  def __init__(self, text, text_type, url=None):
    self.text = text
    self.text_type = text_type
    self.url = url

  def __eq__(self, value):
    if value == None:
      return False
    
    return value.text == self.text and value.text_type == self.text_type and value.url == self.url
  
  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
  


def text_node_to_html_node(text_node):
  if text_node == None:
      return

  
  match text_node.text_type:
      case TextType.TEXT:
          return LeafNode(None, text_node.text)
      
      case TextType.BOLD:
          return LeafNode("b", text_node.text)
      
      case TextType.ITALIC:
          return LeafNode("i", text_node.text)
      
      case TextType.CODE:
          return LeafNode("code", text_node.text)
      
      case TextType.LINK:
          url = ""
          if text_node.url != None:
              url = text_node.url
          return LeafNode("a", text_node.text, {"href": url})
      
      case TextType.IMAGE:
          url = ""
          if text_node.url != None:
              url = text_node.url
          text = ""
          if text_node.text != None:
              text = text_node.text
          return LeafNode("img", "", {"src": url, "alt": text})

      case _:
          raise Exception