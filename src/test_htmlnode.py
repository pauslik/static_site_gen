import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "greeting"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "greeting"})

    def test_repr(self):
        node = HTMLNode(tag="span", value="World", children=None, props=None)
        self.assertEqual(repr(node), "HTMLNode(tag=span, value=World, children=None, props=None)")

    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"id": "main", "class": "container"})
        self.assertEqual(node.props_to_html(), ' id="main" class="container"')

    def test_props_to_html_without_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    # LeafNode tests

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_span_with_props(self):
        node = LeafNode("span", "Important", props={"class": "highlight"})
        self.assertEqual(node.to_html(), '<span class="highlight">Important</span>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    # ParentNode tests

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        child1 = LeafNode("li", "Item 1")
        child2 = LeafNode("li", "Item 2")
        parent_node = ParentNode("ul", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<ul><li>Item 1</li><li>Item 2</li></ul>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_nested_parent_nodes(self):
        leaf1 = LeafNode("li", "Item 1")
        leaf2 = LeafNode("li", "Item 2")
        ul_node = ParentNode("ul", [leaf1, leaf2])
        div_node = ParentNode("div", [ul_node])
        self.assertEqual(
            div_node.to_html(),
            "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>",
        )

    def test_to_html_parent_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], props={"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )

    def test_to_html_parent_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_leaf_no_value(self):
        leaf_node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    

if __name__ == "__main__":
    unittest.main()