from textnode import TextType, TextNode

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