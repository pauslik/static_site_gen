class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    # to be implemented in subclasses
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        return " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])



class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)


    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"



class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children to convert to HTML")
        return f"<{self.tag}{self.props_to_html()}>" + "".join([child.to_html() for child in self.children]) + f"</{self.tag}>"
            