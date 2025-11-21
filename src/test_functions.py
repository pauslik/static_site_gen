import unittest

from functions import text_node_to_html_node
from htmlnode import LeafNode
from textnode import TextType, TextNode

class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_link_props(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertIn("href", html_node.props)
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_image_props(self):
        node = TextNode("An image", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertIsNone(html_node.value)
        self.assertIn("src", html_node.props)
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertIn("alt", html_node.props)
        self.assertEqual(html_node.props["alt"], "An image")

    def test_wrong_type(self):
        node = TextNode("This is wrong type", "UNDERLINE")  # Invalid type
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Unsupported text type", str(context.exception))

    

if __name__ == "__main__":
    unittest.main()