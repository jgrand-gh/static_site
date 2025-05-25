import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "This is sample paragraph text", None, {"href": "https://www.google.com", "target": "_blank",})
        expected_text_string = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_text_string)
    
    def test_props_to_html2(self):
        node = HTMLNode("p", "This is sample paragraph text", None, {"href": "https://www.google.com", "target": "_blank", "img": "none", "alt": "alt-text"})
        expected_text_string = ' href="https://www.google.com" target="_blank" img="none" alt="alt-text"'
        self.assertEqual(node.props_to_html(), expected_text_string)

    def test_props_to_html_none(self):
        node = HTMLNode()
        expected_text_string = ""
        self.assertEqual(node.props_to_html(), expected_text_string)
    
    def test_props_to_html_empty_dict(self):
        node = HTMLNode(None, None, None, {})
        expected_text_string = ""
        self.assertEqual(node.props_to_html(), expected_text_string)        

    def test_repr(self):
        node = HTMLNode("p", "text", None, {"class": "para"})
        expected = 'HTMLNode(p, text, children: None, {\'class\': \'para\'})'
        self.assertEqual(node.__repr__(), expected)

    def test_repr_none(self):
        node = HTMLNode()
        expected = 'HTMLNode(None, None, children: None, None)'
        self.assertEqual(node.__repr__(), expected)
    
    def test_none_tag(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)

    def test_none_value(self):
        node = HTMLNode()
        self.assertEqual(node.value, None)

    def test_none_children(self):
        node = HTMLNode()
        self.assertEqual(node.children, None)

    def test_none_props(self):
        node = HTMLNode()
        self.assertEqual(node.props, None)

    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    # leaf node test cases
    def test_empty_leaf_node(self):
        with self.assertRaises(TypeError):
            node = LeafNode()
    
    def test_none_leaf_node(self):
        with self.assertRaises(ValueError):
            node = LeafNode(None, None).to_html()

    def test_leaf_node_to_html(self):
        node = LeafNode("p", "This is a line of text")
        expected_string_output = "<p>This is a line of text</p>"
        self.assertEqual(node.to_html(), expected_string_output)

    def test_leaf_node_to_html_no_tag(self):
        node = LeafNode(None, "This is a line of text")
        expected_string_output = "This is a line of text"
        self.assertEqual(node.to_html(), expected_string_output)
    
    # parent node test cases
    def test_nested_parent_node(self):
        node = ParentNode(
                "p",   
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
        )
        expected_string_output = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_string_output)

    def test_double_nested_parent_node(self):
        node = ParentNode(
            "body",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "boldeder text"),
                        LeafNode("i", "italicizeder text"),                    
                    ]),
            ],
            {"desc": "body tag"}
        )
        expected_string_output = '<body desc="body tag"><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>boldeder text</b><i>italicizeder text</i></p></body>'
        self.assertEqual(node.to_html(), expected_string_output)
    
    def test_parent_node_single_child(self):
        node = ParentNode(
            "p",
            [LeafNode("b", "some text")],
            {"desc": "paragraph tag"}
        )
        expected_string_output = '<p desc="paragraph tag"><b>some text</b></p>'
        self.assertEqual(node.to_html(), expected_string_output)
    
    def test_parent_node_no_tag_error(self):
        node = ParentNode(
            None,
            [LeafNode("b", "some text")]
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_no_children_error(self):
        node = ParentNode(
            "p", None, {"desc":"paragraph tag"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_empty_children_error(self):
        node = ParentNode(
            "p", [], {"desc":"paragraph tag"})
        with self.assertRaises(ValueError):
            node.to_html()

    #boot.dev suggested tests:
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

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

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()