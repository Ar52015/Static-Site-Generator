from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):

    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINKS = "link"
    IMAGES = "image"

class TextNode():

    def __init__(self, text, textType, url = None):
        
        self.text = text
        self.textType = textType
        self.url = url

    def __eq__(self, other):

        if self.text == other.text and self.textType == other.textType and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        if self.url != None:
            return f"TextNode({self.text}, {self.textType.value}, {self.url})"
        else:
            return f"TextNode({self.text}, {self.textType.value})"
        
def text_node_to_html_node(text_node):
    match text_node.textType:
        case TextType.NORMAL_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINKS:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGES:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Invalid Text Type")
        
def split_nodes_delimiter(old_nodes, delimiter, textType):
    finalList = []
    for node in old_nodes:
        if node.textType is not TextType.NORMAL_TEXT:
            finalList.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts)%2 == 0:
                raise Exception(f"Incorrect Markdown Syntax: {delimiter} isn't closed")

            for i, text in enumerate(parts):
                if i%2 == 0:
                    finalList.append(TextNode(text, TextType.NORMAL_TEXT))
                else:
                    finalList.append(TextNode(text, textType))
    return finalList