import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertEqual(node, node2)

    def test_neq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a different text node", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node, node2)
    
    def test_neq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_neq_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://different.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Sample", TextType.CODE, "https://code.com")
        self.assertEqual(repr(node), "TextNode(Sample, code, https://code.com)")


if __name__ == "__main__":
    unittest.main()