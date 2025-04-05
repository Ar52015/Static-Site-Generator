import unittest

from textnode import TextNode, TextType
from helper import split_nodes_delimiter

class TestHelper(unittest.TestCase):

    def test_split_nodes_delimiter_no_delimiters(self):
        # Test with no delimiters present
        node = TextNode("This is just plain text", TextType.NORMAL_TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        assert len(nodes) == 1
        assert nodes[0].text == "This is just plain text"
        assert nodes[0].textType == TextType.NORMAL_TEXT

    def test_split_nodes_delimiter_one_delimiter_pair(self):
        # Test with one pair of delimiters
        node = TextNode("This is **bold** text", TextType.NORMAL_TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        assert len(nodes) == 3
        assert nodes[0].text == "This is "
        assert nodes[0].textType == TextType.NORMAL_TEXT
        assert nodes[1].text == "bold"
        assert nodes[1].textType == TextType.BOLD_TEXT
        assert nodes[2].text == " text"
        assert nodes[2].textType == TextType.NORMAL_TEXT

    def test_split_nodes_delimiter_multiple_delimiter_pairs(self):
        # Test with multiple delimiter pairs
        node = TextNode("This is **bold** and **more bold** text", TextType.NORMAL_TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        assert len(nodes) == 5
        assert nodes[0].text == "This is "
        assert nodes[0].textType == TextType.NORMAL_TEXT
        assert nodes[1].text == "bold"
        assert nodes[1].textType == TextType.BOLD_TEXT
        assert nodes[2].text == " and "
        assert nodes[2].textType == TextType.NORMAL_TEXT
        assert nodes[3].text == "more bold"
        assert nodes[3].textType == TextType.BOLD_TEXT
        assert nodes[4].text == " text"
        assert nodes[4].textType == TextType.NORMAL_TEXT
