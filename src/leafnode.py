from htmlnode import HTMLNode

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value == None:
      return ValueError("Invalid HTML: no value")
    
    if self.tag == None:
      return self.value
    
    opening_tag = f"<{self.tag}>"
    closing_tag = f"</{self.tag}>"

    if self.props != None:
      opening_tag = opening_tag.replace(">", f" {self.props_to_html()}>")

    if self.tag == "img":
      return opening_tag.replace(">", f"{self.value}/>")

    return f"{opening_tag}{self.value}{closing_tag}"
  
  def __repr__(self):
    return f"LeafNode({self.tag}, {self.value}, {self.props})"