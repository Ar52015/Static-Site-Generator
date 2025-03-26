import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()