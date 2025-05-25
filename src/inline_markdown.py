import re

from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if delimiter in node.text:
                split_nodes = node.text.split(delimiter)

                if len(split_nodes) % 2 == 0:
                    raise ValueError(f"Invalid markdown: Unclosed delimiter {delimiter}")

                for i in range(len(split_nodes)):
                    if split_nodes[i] == "":
                        continue
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(split_nodes[i], text_type))
            else:
                new_nodes.append(node)

    return new_nodes

def split_nodes_image(old_nodes):
    return _split_nodes_by_pattern(old_nodes, extract_markdown_images, "!", TextType.IMAGE)

def split_nodes_link(old_nodes):
    return _split_nodes_by_pattern(old_nodes, extract_markdown_links, "", TextType.LINK)

def _split_nodes_by_pattern(old_nodes, extract_func, prefix, node_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        current_text = node.text
        extracted_items = extract_func(current_text)
        
        if len(extracted_items) == 0:
            new_nodes.append(node)
            continue

        for item_text, url in extracted_items:
            pattern = f"{prefix}[{item_text}]({url})"
            split_nodes = current_text.split(pattern, 1)

            if split_nodes[0]:
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))

            new_nodes.append(TextNode(item_text, node_type, url))        
            
            if len(split_nodes) > 1:
                current_text = split_nodes[1]
            else:
                current_text = ""
        
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    regex_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex_pattern, text)
    return matches

def extract_markdown_links(text):
    regex_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex_pattern, text)
    return matches