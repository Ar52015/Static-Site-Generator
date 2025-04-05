import unittest

from textnode import TextNode, TextType
from helper import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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

class TestMarkdownImageLinkParsing(unittest.TestCase):

    def test_split_nodes_image_basic(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_nodes_image_no_image(self):
        node = TextNode("This is text with no image", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_nodes_image_only_image(self):
        node = TextNode("![standalone image](https://example.com/img.jpg)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("standalone image", TextType.IMAGES, "https://example.com/img.jpg")],
            new_nodes,
        )

    def test_split_nodes_image_start_with_image(self):
        node = TextNode("![first image](https://example.com/first.jpg) followed by text", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first image", TextType.IMAGES, "https://example.com/first.jpg"),
                TextNode(" followed by text", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )
    
    def test_split_nodes_image_end_with_image(self):
        node = TextNode("Text followed by an ![end image](https://example.com/end.jpg)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text followed by an ", TextType.NORMAL_TEXT),
                TextNode("end image", TextType.IMAGES, "https://example.com/end.jpg"),
            ],
            new_nodes,
        )
    
    def test_split_nodes_image_multiple_nodes(self):
        nodes = [
            TextNode("First node ![image1](https://example.com/1.jpg)", TextType.NORMAL_TEXT),
            TextNode("Second node", TextType.NORMAL_TEXT),
            TextNode("Third node ![image2](https://example.com/2.jpg)", TextType.NORMAL_TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("First node ", TextType.NORMAL_TEXT),
                TextNode("image1", TextType.IMAGES, "https://example.com/1.jpg"),
                TextNode("Second node", TextType.NORMAL_TEXT),
                TextNode("Third node ", TextType.NORMAL_TEXT),
                TextNode("image2", TextType.IMAGES, "https://example.com/2.jpg"),
            ],
            new_nodes,
        )
    
    def test_split_nodes_image_non_text_node(self):
        nodes = [
            TextNode("Normal text", TextType.NORMAL_TEXT),
            TextNode("Link text", TextType.LINKS, "https://example.com"),
            TextNode("Text with ![image](https://example.com/img.jpg)", TextType.NORMAL_TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Normal text", TextType.NORMAL_TEXT),
                TextNode("Link text", TextType.LINKS, "https://example.com"),
                TextNode("Text with ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGES, "https://example.com/img.jpg"),
            ],
            new_nodes,
        )
    
    # Tests for split_nodes_link
    def test_split_nodes_link_basic(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL_TEXT),
                TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode(
                    "to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_nodes_link_no_link(self):
        node = TextNode("This is text with no link", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_nodes_link_only_link(self):
        node = TextNode("[standalone link](https://example.com)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("standalone link", TextType.LINKS, "https://example.com")],
            new_nodes,
        )
    
    def test_split_nodes_link_start_with_link(self):
        node = TextNode("[first link](https://example.com/first) followed by text", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first link", TextType.LINKS, "https://example.com/first"),
                TextNode(" followed by text", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )
    
    def test_split_nodes_link_end_with_link(self):
        node = TextNode("Text followed by a [end link](https://example.com/end)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text followed by a ", TextType.NORMAL_TEXT),
                TextNode("end link", TextType.LINKS, "https://example.com/end"),
            ],
            new_nodes,
        )
    
    def test_split_nodes_link_multiple_nodes(self):
        nodes = [
            TextNode("First node [link1](https://example.com/1)", TextType.NORMAL_TEXT),
            TextNode("Second node", TextType.NORMAL_TEXT),
            TextNode("Third node [link2](https://example.com/2)", TextType.NORMAL_TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("First node ", TextType.NORMAL_TEXT),
                TextNode("link1", TextType.LINKS, "https://example.com/1"),
                TextNode("Second node", TextType.NORMAL_TEXT),
                                TextNode("Third node ", TextType.NORMAL_TEXT),
                TextNode("link2", TextType.LINKS, "https://example.com/2"),
            ],
            new_nodes,
        )
    
    def test_split_nodes_link_non_text_node(self):
        nodes = [
            TextNode("Normal text", TextType.NORMAL_TEXT),
            TextNode("Image text", TextType.IMAGES, "https://example.com/img.jpg"),
            TextNode("Text with [link](https://example.com)", TextType.NORMAL_TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Normal text", TextType.NORMAL_TEXT),
                TextNode("Image text", TextType.IMAGES, "https://example.com/img.jpg"),
                TextNode("Text with ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINKS, "https://example.com"),
            ],
            new_nodes,
        )
    
    def test_split_nodes_link_with_special_characters(self):
        node = TextNode(
            "Link with [special chars!@#](https://example.com/special?q=test&p=1)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with ", TextType.NORMAL_TEXT),
                TextNode("special chars!@#", TextType.LINKS, "https://example.com/special?q=test&p=1"),
            ],
            new_nodes,
        )
    
    def test_split_nodes_image_with_special_characters(self):
        node = TextNode(
            "Image with ![special chars!@#](https://example.com/special.jpg?size=large)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with ", TextType.NORMAL_TEXT),
                                TextNode("special chars!@#", TextType.IMAGES, "https://example.com/special.jpg?size=large"),
            ],
            new_nodes,
        )
    
    def test_empty_text_nodes_not_included(self):
        node = TextNode("[link1](https://example.com/1)[link2](https://example.com/2)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINKS, "https://example.com/1"),
                TextNode("link2", TextType.LINKS, "https://example.com/2"),
            ],
            new_nodes,
        )
        
        node = TextNode("![img1](https://example.com/1.jpg)![img2](https://example.com/2.jpg)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGES, "https://example.com/1.jpg"),
                TextNode("img2", TextType.IMAGES, "https://example.com/2.jpg"),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()