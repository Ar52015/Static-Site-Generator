from enum import Enum

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
        return f"TextNode({self.text}, {self.textType.value}, {self.url})"
    

