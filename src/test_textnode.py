import unittest

from textnode import TextType, TextNode, text_node_to_html_node
from main import *


class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)

  def test_eq2(self):
    node = TextNode("This is a text node", TextType.BOLD, None)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)
  
  def test_not_eq(self):
    node = TextNode("This is a text node 1", TextType.IMAGE)
    node2 = TextNode("This is a text node 2", TextType.ITALIC, "https://reframe.network")
    self.assertNotEqual(node, node2)

  def test_eq_false(self):
    node = TextNode("This is a text node", TextType.TEXT)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertNotEqual(node, node2)

  def test_eq_false2(self):
    node = TextNode("This is a text node", TextType.TEXT)
    node2 = TextNode("This is a text node2", TextType.TEXT)
    self.assertNotEqual(node, node2)

  def test_eq_url(self):
    node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
    node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
    self.assertEqual(node, node2)

  def test_repr(self):
    node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
    self.assertEqual(
        "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
    )

  def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

  def test_code(self):
    node = TextNode("json.STRINGIFY(formdata)", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "json.STRINGIFY(formdata)")

  def test_image(self):
    node = TextNode("alt here", TextType.IMAGE, "./img/placeholder.png")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "")
  
  def test_link(self):
    node = TextNode("click here", TextType.LINK, "https://reframe.network")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "click here")

  def test_italic(self):
    node = TextNode("I am an Italian in Italics", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "I am an Italian in Italics")

  

if __name__ == "__main__":
  unittest.main()