import unittest

from textnode import *
from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):
  def test_split_node_delimeter_code(self):
    node = TextNode("This is text with a `code block` in the middle", TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(result, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" in the middle", TextType.TEXT),])

  def test_split_node_delimeter_bold(self):
    node = TextNode("This is text with a **bold block** word", TextType.TEXT)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(result, [TextNode("This is text with a ", TextType.TEXT), TextNode("bold block", TextType.BOLD), TextNode(" word", TextType.TEXT),])
  
  def test_split_node_delimeter_italics(self):
    node = TextNode("This is an _italic and **bold** word_.", TextType.TEXT)
    result = split_nodes_delimiter([node], "_", TextType.ITALIC)
    self.assertEqual(result, [TextNode("This is an ", TextType.TEXT), TextNode("italic and **bold** word", TextType.ITALIC), TextNode(".", TextType.TEXT),])

  def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
  
  def test_extract_markdown_links(self):
    matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
    self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
  
  def test_split_nodes_link(self):
    node = TextNode("This is a [simple link](https://example.com) in a sentence.", TextType.TEXT)
    self.assertEqual(split_nodes_link([node]), [TextNode("This is a ", TextType.TEXT), TextNode("simple link",TextType.LINK,"https://example.com"), TextNode(" in a sentence.", TextType.TEXT)])
  
  def test_multiple_links(self):
    node = TextNode("Go to [Google](https://google.com) or [Bing](https://bing.com) now.", TextType.TEXT)
    self.assertEqual(
        split_nodes_link([node]),
        [
            TextNode("Go to ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" or ", TextType.TEXT),
            TextNode("Bing", TextType.LINK, "https://bing.com"),
            TextNode(" now.", TextType.TEXT)
        ]
    )

  def test_link_at_start(self):
    node = TextNode("[Start here](https://start.com) for more.", TextType.TEXT)
    self.assertEqual(
        split_nodes_link([node]),
        [
            TextNode("Start here", TextType.LINK, "https://start.com"),
            TextNode(" for more.", TextType.TEXT)
        ]
    )

  def test_link_at_end(self):
    node = TextNode("Learn more at [Docs](https://docs.com)", TextType.TEXT)
    self.assertEqual(
        split_nodes_link([node]),
        [
            TextNode("Learn more at ", TextType.TEXT),
            TextNode("Docs", TextType.LINK, "https://docs.com")
        ]
    )

  def test_no_links(self):
    node = TextNode("This string has no links.", TextType.TEXT)
    self.assertEqual(
        split_nodes_link([node]),
        [
            TextNode("This string has no links.", TextType.TEXT)
        ]
    )

  def test_adjacent_links(self):
    node = TextNode("Visit [SiteA](https://a.com)[SiteB](https://b.com)", TextType.TEXT)
    self.assertEqual(
        split_nodes_link([node]),
        [
            TextNode("Visit ", TextType.TEXT),
            TextNode("SiteA", TextType.LINK, "https://a.com"),
            TextNode("SiteB", TextType.LINK, "https://b.com")
        ]
    )

  def test_same_text_different_links(self):
    node = TextNode("Click [here](https://a.com) or [here](https://b.com)", TextType.TEXT)
    self.assertEqual(
        split_nodes_link([node]),
        [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://a.com"),
            TextNode(" or ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://b.com")
        ]
    )

  def test_single_image_in_text(self):
      node = TextNode("Here is an image ![cat](https://example.com/cat.jpg).", TextType.TEXT)
      self.assertEqual(
          split_nodes_image([node]),
          [
              TextNode("Here is an image ", TextType.TEXT),
              TextNode("cat", TextType.IMAGE, "https://example.com/cat.jpg"),
              TextNode(".", TextType.TEXT)
          ]
      )

  def test_image_at_start(self):
      node = TextNode("![logo](https://logo.com) is our logo.", TextType.TEXT)
      self.assertEqual(
          split_nodes_image([node]),
          [
              TextNode("logo", TextType.IMAGE, "https://logo.com"),
              TextNode(" is our logo.", TextType.TEXT)
          ]
      )

  def test_image_at_end(self):
    node = TextNode("This is the picture ![sunset](https://img.com/sunset.png)", TextType.TEXT)
    self.assertEqual(
        split_nodes_image([node]),
        [
            TextNode("This is the picture ", TextType.TEXT),
            TextNode("sunset", TextType.IMAGE, "https://img.com/sunset.png")
        ]
    )


  def test_multiple_images(self):
    node = TextNode("![img1](url1) middle text ![img2](url2)", TextType.TEXT)
    self.assertEqual(
        split_nodes_image([node]),
        [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" middle text ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2")
        ]
    )


  def test_adjacent_images(self):
    node = TextNode("![a](a.com)![b](b.com)", TextType.TEXT)
    self.assertEqual(
        split_nodes_image([node]),
        [
            TextNode("a", TextType.IMAGE, "a.com"),
            TextNode("b", TextType.IMAGE, "b.com")
        ]
    )

  def test_no_images(self):
    node = TextNode("This has no images.", TextType.TEXT)
    self.assertEqual(
        split_nodes_image([node]),
        [
            TextNode("This has no images.", TextType.TEXT)
        ]
    )

  def test_split_image(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ],
        new_nodes,
    )

  def test_split_image_single(self):
    node = TextNode(
        "![image](https://www.example.COM/IMAGE.PNG)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
        ],
        new_nodes,
    )

  def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

  def test_split_links(self):
    node = TextNode(
        "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
            TextNode(" with text that follows", TextType.TEXT),
        ],
        new_nodes,
    )

  def test_combined_textnodes(self):
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes_list = text_to_textnodes(text)
    self.assertListEqual([
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
    ],nodes_list)

if __name__ == "__main__":
  unittest.main()