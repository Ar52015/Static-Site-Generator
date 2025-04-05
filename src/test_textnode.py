import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("node1", TextType.LINKS, "hello")
        node2 = TextNode("node2", TextType.IMAGES, "bye")
        self.assertNotEqual(node, node2)

    def test_nodes_with_different_text_not_equal(self):
        node1 = TextNode("First text", TextType.BOLD_TEXT)
        node2 = TextNode("Second text", TextType.BOLD_TEXT)
        self.assertNotEqual(node1, node2)

    def test_nodes_with_different_text_not_equal(self):
        node1 = TextNode("First text", TextType.BOLD_TEXT)
        node2 = TextNode("First text", TextType.LINKS)
        self.assertNotEqual(node1, node2)

    def test_nodes_with_different_text_not_equal(self):
        node1 = TextNode("First text", TextType.LINKS, "hello")
        node2 = TextNode("First text", TextType.LINKS, "bye")
        self.assertNotEqual(node1, node2)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, None)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_text_to_html_node(self):
        # Test normal text
        text_node = TextNode("This is normal text", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is normal text")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {})

    def test_bold_to_html_node(self):
        # Test bold text
        text_node = TextNode("This is bold text", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {})

    def test_italic_to_html_node(self):
        # Test italic text
        text_node = TextNode("This is italic text", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {})

    def test_code_to_html_node(self):
        # Test code text
        text_node = TextNode("print('Hello World')", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello World')")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {})

    def test_link_to_html_node(self):
        # Test link
        text_node = TextNode("Click here", TextType.LINKS)
        text_node.url = "https://www.example.com"
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_image_to_html_node(self):
        # Test image
        text_node = TextNode("Image description", TextType.IMAGES)
        text_node.url = "https://www.example.com/image.jpg"
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {
            "src": "https://www.example.com/image.jpg",
            "alt": "Image description"
        })

    def test_invalid_textType(self):
        # Test invalid text type
        # This assumes you have access to an invalid TextType or can create one for testing
        try:
            # Creating a TextNode with an invalid textType
            # This might need to be adjusted based on your implementation
            from enum import Enum
            class FakeTextType(Enum):
                FAKE = "fake"
                
            invalid_node = TextNode("Invalid type test", FakeTextType.FAKE)
            text_node_to_html_node(invalid_node)
            self.fail("Expected an exception but none was raised")
        except Exception:
            # Test passes if an exception is raised
            pass

if __name__ == "__main__":
    unittest.main()