import unittest

from htmlnode import HTMLNode

class TextHTMLNode(unittest.TestCase):
  def test_empty_props(self):
    html = HTMLNode("p", "hello ebryone", None, None)
    self.assertEqual(html.props_to_html(), "")
  
  def test_props(self):
    html = HTMLNode("div", None, None, {"id": "root"})
    self.assertEqual('id="root"', html.props_to_html())

  def test_multiple_props(self):
    html = HTMLNode("a", "click here", None, {
    "href": "https://www.google.com",
    "target": "_blank",
    })
    self.assertEqual('href="https://www.google.com" target="_blank"', html.props_to_html())

  def test_multiple_props_false(self):
    html = HTMLNode("a", "click here", None, {
    "href": "https://www.google.com",
    "target": "_blank",
    })
    self.assertNotEqual('href="https://www.google.com"target="_blank"', html.props_to_html())


if __name__ == "__main__":
  unittest.main()