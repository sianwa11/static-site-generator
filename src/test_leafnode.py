import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

  def test_leaf_to_html_a(self):
    node = LeafNode("a", "Click Me!", {"href": "https://reframe.network"})
    self.assertEqual(node.to_html(), '<a href="https://reframe.network">Click Me!</a>')

  def test_leaf_to_html_img(self):
    node = LeafNode("img", "", {"src": "img/placeholder.png", "alt": "bruuh"})
    self.assertEqual(node.to_html(), '<img src="img/placeholder.png" alt="bruuh"/>')

  def test_leaf_to_html_div(self):
    node = LeafNode("div", "Waaaah", {"class": "fa fa-trash", "id": "trash-can"})
    self.assertEqual(node.to_html(), '<div class="fa fa-trash" id="trash-can">Waaaah</div>')
