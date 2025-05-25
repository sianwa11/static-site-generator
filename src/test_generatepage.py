import unittest
from generatepage import extract_title

class TestGeneratePage(unittest.TestCase):
  def test_extracts_title_correctly(self):
    md = "# My Title\n\nSome content"
    self.assertEqual(extract_title(md), "My Title")

  def test_ignores_other_headings(self):
    md = "# First Title\n\n## Second Title\n\n# Third Title"
    self.assertEqual(extract_title(md), "First Title")

  def test_raises_exception_if_no_h1(self):
    md = "## Subtitle\n\nSome text\n### Another one"
    with self.assertRaises(Exception) as context:
        extract_title(md)
    self.assertEqual(str(context.exception), "A title is required")

  def test_works_with_extra_spaces(self):
    md = "#    Trimmed Title   \nSome text"
    self.assertEqual(extract_title(md), "Trimmed Title   ")  # only left space stripped by regex, not trailing

  def test_handles_empty_string(self):
    with self.assertRaises(Exception):
        extract_title("")

  def test_ignores_inline_hashes(self):
    md = "Text with # not a title\n\n# Proper Title"
    self.assertEqual(extract_title(md), "Proper Title")


if __name__ == "__main__":
  unittest.main()