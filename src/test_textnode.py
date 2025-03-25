import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()