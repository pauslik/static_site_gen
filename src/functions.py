from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unsupported text type: {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    # TODO: iterate over each character and track text_type, save it once the same delimiter is found
    # TODO: add check for no closing delimiter
    new_nodes = []
    temp_nodes = []
    deli_map = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE
    }

    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter == "":
            new_nodes.append(node)
        elif delimiter in deli_map:
            temp_nodes = node.text.split(delimiter)
            if len(temp_nodes) < 3:
                new_nodes.append(node)
            else:
                new_nodes.append(TextNode(temp_nodes[0], TextType.TEXT))
                new_nodes.append(TextNode(temp_nodes[1], text_type))
                new_nodes.append(TextNode(temp_nodes[2], TextType.TEXT))
        else:
            raise ValueError(f'Matching delimiter not found: {delimiter}')
        
    # remove empty nodes
    cleaned_nodes = []
    for i in range(len(new_nodes)):
        if new_nodes[i].text != "":
            cleaned_nodes.append(new_nodes[i])

    return cleaned_nodes