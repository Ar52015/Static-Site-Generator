import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_empty(self):
        # Test with empty props
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_single_prop(self):
        # Test with a single property
        node = HTMLNode("a", "Click me", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
    
    def test_props_to_html_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode(
            "a", 
            "Click me", 
            props={
                "href": "https://example.com", 
                "target": "_blank",
                "class": "button"
            }
        )
        html = node.props_to_html()
        self.assertIn(' href="https://example.com"', html)
        self.assertIn(' target="_blank"', html)
        self.assertIn(' class="button"', html)
        # Count the number of spaces to ensure properties are properly separated
        self.assertEqual(html.count(' '), 3)  # One space before each of the 3 properties

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")
    
    def test_leaf_to_html_with_multiple_attributes(self):
        node = LeafNode("input", "", {"type": "text", "placeholder": "Enter your name"})
        self.assertEqual(node.to_html(), '<input type="text" placeholder="Enter your name"></input>')
    
    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()