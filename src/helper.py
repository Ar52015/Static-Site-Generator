import re

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

#Helper Functions
def extract_markdown_images(text):
    matches = re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    res = []
    for node in old_nodes:
        if node.textType != TextType.NORMAL_TEXT:
            res.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if not matches:
            res.append(node)
            continue
        
        curr_text = node.text
        curr_index = 0

        for alt_text, url in matches:
            image_markdown = f"![{alt_text}]({url})"
            start_index = curr_text.find(image_markdown, curr_index)
            if start_index == -1:
                continue
            if start_index > curr_index:
                res.append(TextNode(curr_text[curr_index:start_index], TextType.NORMAL_TEXT))
            res.append(TextNode(alt_text, TextType.IMAGES, url))
            curr_index = start_index + len(image_markdown)
        if curr_index < len(curr_text):
            res.append(TextNode(curr_text[curr_index:], TextType.NORMAL_TEXT))
    return res

def split_nodes_link(old_nodes):
    res = []
    for node in old_nodes:
        if node.textType != TextType.NORMAL_TEXT:
            res.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if not matches:
            res.append(node)
            continue
        
        curr_text = node.text
        curr_index = 0

        for alt_text, url in matches:
            link_markdown = f"[{alt_text}]({url})"
            start_index = curr_text.find(link_markdown, curr_index)
            if start_index == -1:
                continue
            if start_index > curr_index:
                res.append(TextNode(curr_text[curr_index:start_index], TextType.NORMAL_TEXT))
            res.append(TextNode(alt_text, TextType.LINKS, url))
            curr_index = start_index + len(link_markdown)
        if curr_index < len(curr_text):
            res.append(TextNode(curr_text[curr_index:], TextType.NORMAL_TEXT))
    return res
            