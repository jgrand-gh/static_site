import textwrap, re

from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType
from inline_markdown import text_to_textnodes

HEADING_REGEX_PATTERN = r"^(#{1,6} ).*"
CODE_REGEX_PATTERN = r'^```.*?\n(.*?)```\s*$'
QUOTE_REGEX_PATTERN = r"^>.*(\n>.*)*$"
UNORDERED_LIST_REGEX_PATTERN = r"^[\*\-\+]\s+"
ORDERED_LIST_REGEX_PATTERN = r"^(\d+)\.\s+"
WHITESPACE_COLLAPSE_PATTERN = r'\s+'

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    markdown = textwrap.dedent(markdown)
    markdown_nodes = markdown.split("\n\n")

    filtered_list = []
    for node in markdown_nodes:
        if node == "":
            continue
        node = node.strip()
        filtered_list.append(node)

    return filtered_list

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [])

    for block in markdown_blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            parent_node.children.append(generate_heading_node(block))
        elif block_type == BlockType.CODE:
            parent_node.children.append(generate_code_node(block))
        elif block_type == BlockType.QUOTE:
            parent_node.children.append(generate_quote_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            parent_node.children.append(generate_unordered_list_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            parent_node.children.append(generate_ordered_list_node(block))
        else:
            children = text_to_children(re.sub(WHITESPACE_COLLAPSE_PATTERN, ' ', block))
            p_node = ParentNode("p", children)
            parent_node.children.append(p_node)
    
    return parent_node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    html_nodes = []
    for text_node in text_nodes:
        html_node = TextNode.text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    
    return html_nodes

def generate_heading_node(block):
    hashtags = 0
    for char in block:
        if char == '#':
            hashtags += 1
        else:
            break
    
    if hashtags < 1 or hashtags > 6:
        hashtags = 1
    
    content = block[hashtags:].strip()
    children = text_to_children(content)
    
    return ParentNode(f"h{hashtags}", children, None)

def generate_code_node(block):
    code_content = re.sub(CODE_REGEX_PATTERN, r'\1', block, flags=re.DOTALL)
    text_node = TextNode(code_content, TextType.TEXT)
    code_leaf_node = TextNode.text_node_to_html_node(text_node)
    code_node = ParentNode("code", [code_leaf_node])
    pre_node = ParentNode("pre", [code_node])

    return pre_node

def generate_quote_node(block):
    lines = block.split("\n")
    quote_content = []
    for line in lines:
        if line.startswith('>'):
            quote_content.append(line[1:].lstrip())
        else:
            quote_content.append(line)

    content = " ".join(quote_content)
    children = text_to_children(content)
    quote_node = ParentNode("blockquote", children)

    return quote_node

def generate_unordered_list_node(block):
    list_node = ParentNode("ul", [], None)
    
    items = block.split("\n")
    
    for item in items:
        if not item.strip():
            continue
        content = re.sub(UNORDERED_LIST_REGEX_PATTERN, "", item.strip())
        children = text_to_children(content)
        li_node = ParentNode("li", children, None)
        list_node.children.append(li_node)
    
    return list_node

def generate_ordered_list_node(block):
    list_node = ParentNode("ol", [], None)
    
    items = block.split("\n")
    
    for item in items:
        if not item.strip():
            continue
        content = re.sub(ORDERED_LIST_REGEX_PATTERN, "", item.strip())
        children = text_to_children(content)
        li_node = ParentNode("li", children, None)
        list_node.children.append(li_node)
    
    return list_node

def block_to_block_type(block):
    if re.match(HEADING_REGEX_PATTERN, block):
        return BlockType.HEADING
    elif re.match(CODE_REGEX_PATTERN, block, re.DOTALL):
        return BlockType.CODE
    elif re.match(QUOTE_REGEX_PATTERN, block, re.DOTALL):
        return BlockType.QUOTE
    elif _is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif _is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def _is_unordered_list(block):
    for line in block.split('\n'):
        if not re.match(UNORDERED_LIST_REGEX_PATTERN, line):
            return False
    return True

def _is_ordered_list(block):
    expected_number = 1
    for line in block.split('\n'):
        match = re.match(ORDERED_LIST_REGEX_PATTERN, line)
        if not match:
            return False
        
        number = int(match.group(1))
        if number != expected_number:
            return False
        expected_number += 1
    return True