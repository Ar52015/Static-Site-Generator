import unittest

from textnode import TextNode, TextType
from helper import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestSplitNodesDelimiter(unittest.TestCase):

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

class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_single_image(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_multiple_images(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
    
    def test_extract_no_images(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)
    
    def test_extract_single_link(self):
        matches = extract_markdown_links("This is text with a [link](https://www.boot.dev)")
        self.assertListEqual([("link", "https://www.boot.dev")], matches)
    
    def test_extract_multiple_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_no_links(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual([], matches)
    
    def test_extract_links_not_images(self):
        # Make sure links function doesn't extract images
        matches = extract_markdown_links("This is text with a ![image](https://example.com/image.png) and [actual link](https://example.com)")
        self.assertListEqual([("actual link", "https://example.com")], matches)
    
    def test_extract_images_not_links(self):
        # Make sure images function doesn't extract links
        matches = extract_markdown_images("This is text with a [link](https://example.com) and ![actual image](https://example.com/image.png)")
        self.assertListEqual([("actual image", "https://example.com/image.png")], matches)
    
    def test_complex_text_with_both(self):
        text = """
        # My Markdown Document
        
        This is a paragraph with a [link to Boot.dev](https://boot.dev) and an ![image of a cat](https://example.com/cat.jpg).
        
        Here's another paragraph with another [link](https://example.org) and another ![image](https://example.com/dog.png).
        """
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        self.assertListEqual([
            ("image of a cat", "https://example.com/cat.jpg"),
            ("image", "https://example.com/dog.png")
        ], image_matches)
        
        self.assertListEqual([
            ("link to Boot.dev", "https://boot.dev"),
            ("link", "https://example.org")
        ], link_matches)

if __name__ == "__main__":
    unittest.main()