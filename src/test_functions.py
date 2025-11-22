import unittest

from functions import *
from htmlnode import LeafNode
from textnode import TextType, TextNode

class TestFunctionsText(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
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

class TestFunctionsSplit(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "", TextType.TEXT)
        self.assertEqual(new_nodes[0], TextNode("This is text", TextType.TEXT))
    
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with an ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_no_delimiter_found(self):
        node = TextNode("This is text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "", TextType.TEXT)
        self.assertEqual(new_nodes[0], TextNode("This is text", TextType.TEXT))

    def test_wrong_delimiter(self):
        node = TextNode("This is text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "^", TextType.TEXT)

    def test_multiple_nodes(self):
        node1 = TextNode("Text `with` code", TextType.TEXT)
        node2 = TextNode("**with** bold", TextType.TEXT)
        node3 = TextNode("Text _with_", TextType.TEXT)
        code_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        bold_nodes = split_nodes_delimiter(code_nodes, "**", TextType.BOLD)
        italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)

        self.assertEqual(len(code_nodes), 5)
        self.assertEqual(len(bold_nodes), 6)
        self.assertEqual(len(italic_nodes), 7)
        
        self.assertEqual(code_nodes[0], TextNode("Text ", TextType.TEXT))
        self.assertEqual(code_nodes[1], TextNode("with", TextType.CODE))
        self.assertEqual(code_nodes[2], TextNode(" code", TextType.TEXT))
        
        self.assertEqual(bold_nodes[3], TextNode("with", TextType.BOLD))
        self.assertEqual(bold_nodes[4], TextNode(" bold", TextType.TEXT))
        
        self.assertEqual(italic_nodes[5], TextNode("Text ", TextType.TEXT))
        self.assertEqual(italic_nodes[6], TextNode("with", TextType.ITALIC))

class TestFunctionsRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multi_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_multi_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_image_link(self):
        matches = extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_link_image(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_empty(self):
        images = extract_markdown_images("This is text (no images)")
        links = extract_markdown_links("This is text (no links)")
        self.assertListEqual([], images)
        self.assertListEqual([], links)

if __name__ == "__main__":
    unittest.main()