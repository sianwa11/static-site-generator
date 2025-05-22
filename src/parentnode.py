from htmlnode import HTMLNode

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)
  
  def to_html(self):
    if self.tag == None:
      raise ValueError("Tag is required")
    
    if self.children == None:
      raise ValueError("Children are required")
    
    props = ""
    if self.props != None:
      props = " " + self.props_to_html()
    
    return f"<{self.tag}{props}>" + self.__process_nodes(self.children) + f"</{self.tag}>"
    
  def __process_nodes(self, leafNodeList):
    if len(leafNodeList) == 0:
      return ""
    
    return leafNodeList[0].to_html() + self.__process_nodes(leafNodeList[1:])
