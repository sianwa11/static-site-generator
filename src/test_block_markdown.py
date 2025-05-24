import unittest

from block_markdown import markdown_to_blocks,block_to_block_type,markdown_to_html_node,BlockType

class TestBlockMarkDown(unittest.TestCase):

  def test_markdown_to_blocks(self):
    md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
    blocks = markdown_to_blocks(md)
    self.assertListEqual(blocks, ["This is **bolded** paragraph","This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line","- This is a list\n- with items"])

  def test_empty_input(self):
    md = ""
    blocks = markdown_to_blocks(md)
    self.assertListEqual(blocks, [])

  def test_single_paragraph(self):
    md = "Just one paragraph with some **bold** text."
    blocks = markdown_to_blocks(md)
    self.assertListEqual(blocks, ["Just one paragraph with some **bold** text."])

  def test_leading_trailing_newlines(self):
    md = "\n\nParagraph with extra space\n\n"
    blocks = markdown_to_blocks(md)
    self.assertListEqual(blocks, ["Paragraph with extra space"])

  def test_multiple_empty_lines_between_blocks(self):
    md = "First block\n\n\n\nSecond block"
    blocks = markdown_to_blocks(md)
    self.assertListEqual(blocks, ["First block", "Second block"])

  def test_multiple_list_blocks(self):
    md = """
    - item 1
    - item 2

    - item 3
    - item 4
    """
    blocks = markdown_to_blocks(md)
    self.assertListEqual(blocks, ["- item 1\n- item 2", "- item 3\n- item 4"])

  def test_markdown_to_blocks_newlines(self):
      md = """
      This is **bolded** paragraph

      This is another paragraph with _italic_ text and `code` here
      This is the same paragraph on a new line

      - This is a list
      - with items
      """
      blocks = markdown_to_blocks(md)
      self.assertEqual(
          blocks,
          [
              "This is **bolded** paragraph",
              "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
              "- This is a list\n- with items",
          ],
      )


  def test_block_to_block_types(self):
    block = "# heading"
    self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    block = "```\ncode\n```"
    self.assertEqual(block_to_block_type(block), BlockType.CODE)
    block = "> quote\n> more quote"
    self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    block = "- list\n- items"
    self.assertEqual(block_to_block_type(block), BlockType.ULIST)
    block = "1. list\n2. items"
    self.assertEqual(block_to_block_type(block), BlockType.OLIST)
    block = "paragraph"
    self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

  def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

  def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

#   def test_paragraphs(self):
#     md = """
# This is **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and `code` here

# ## Wallahi yuaa gae

# ```
# int id = 11;
# ```

# > a person who thinks all the time
# > is guwaee


# - This is a list
# - with items

# 1. list
# 2. items
#     """
#     node = markdown_to_html_node(md)
#     print(node.to_html())
   




if __name__ == "__main__":
  unittest.main()