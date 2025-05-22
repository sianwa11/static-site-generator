import re

from textnode import *
from htmlnode import HTMLNode
from parentnode import ParentNode




def extract_markdown_images(text):
    # return re.findall(r"\w+ !\[(\w+)\]\((.*?)\)", text)
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        splitted = old_node.text.split(delimiter)

        if len(splitted) % 2 == 0:
            raise Exception("Invalid markdown syntax")
        split_nodes = []
        for i in range(len(splitted)):
            if splitted[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(splitted[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(splitted[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def main():
    pass

main()