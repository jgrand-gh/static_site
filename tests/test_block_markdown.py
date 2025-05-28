import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node, extract_title

class TestBlockMarkdown(unittest.TestCase):

    # markdown_to_blocks tests
    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_single_block(self):
        md = """This is a single block of text."""
        blocks = markdown_to_blocks(md)
        assert blocks == ["This is a single block of text."]
    
    def test_markdown_to_blocks_multiple_blocks(self):
        md = """
        Block 1

        Block 2

        Block 3
        """
        blocks = markdown_to_blocks(md)
        assert blocks == ["Block 1", "Block 2", "Block 3"]

    def test_markdown_to_blocks_indented(self):
        md = """
            First block with spaces

            - Second block: a list
            - with leading spaces
        """
        blocks = markdown_to_blocks(md)
        assert blocks == [
            "First block with spaces",
            "- Second block: a list\n- with leading spaces",
        ]
    
    def test_markdown_to_blocks_excessive_blank_lines(self):
        md = """

        First block


        Second block



        Third block
        """
        blocks = markdown_to_blocks(md)
        assert blocks == ["First block", "Second block", "Third block"]

    def test_markdown_to_blocks_leading_trailing_newlines(self):
        md = """

        This is a block with some extra newline space  
        """
        blocks = markdown_to_blocks(md)
        assert blocks == ["This is a block with some extra newline space"]

    def test_markdown_to_blocks_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        assert blocks == []    

    # tests for block_to_block_type
    def test_paragraph(self):
        block = "This is a simple paragraph with no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading1(self):
        block = "# This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading2(self):
        block = "## This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading3(self):
        block = "### This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading4(self):
        block = "#### This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading5(self):
        block = "##### This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading6(self):
        block = "###### This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_invalid_heading(self):
        block = "####### This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code(self):
        block = "```This is a code block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_invalid_code(self):
        block = "``This is a code block```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_multiline(self):
        block = "```This is a code block\nwith multiple lines\nof code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = ">To be, or not to be\n>That is the question"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_invalid_quote(self):
        block = "To be, or not to be\n>That is the question"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- Shopping\n- List\n- Unordered"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_invalid_unordered_list(self):
        block = "- Shopping\n2. List\n- Unordered"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. Shopping\n2. List\n3. Ordered"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_invalid_ordered_list(self):
        block = "1. Shopping\n- List\n3. Ordered"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_out_of_ordered_list(self):
        block = "1. Shopping\n3. List\n2. Ordered"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

        #boot.dev unit tests
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_extract_title(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(title, "Hello")

    def test_extract_title_multiline(self):
        md = """
Hello
Hello!!!
# Helllllllooooo
"""
        title = extract_title(md)
        self.assertEqual(title, "Helllllllooooo")
    
    def test_invalid_extract_title_no_discernable_h1(self):
        md = "#Hello"
        with self.assertRaises(Exception):
            extract_title(md)
    
    def test_invalid_extract_title_no_hashtag(self):
        md = "Hello"
        with self.assertRaises(Exception):
            extract_title(md)
    
if __name__ == "__main__":
    unittest.main()