from textnode import *
from leafnode import LeafNode
from htmlnode import HTMLNode

def main():
#  new_node = TextNode("This is some anchor text", TextType.LINK , "https://www.boot.dev")
 leaf_node = LeafNode("p", "This is a paragraph of text.").to_html()
 leaf_node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
 leaf_node3 = LeafNode("div", "Waaaah", {"class": "fa fa-trash", 'id': 'btn'}).to_html()
 print(leaf_node)
 print(leaf_node2)
 print(leaf_node3)
 

main()