class HTMLNode():

    def __init__(self, tag = None, value = None, children = None, props = None):
        
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("self.value has not been assigned a value")
        elif not self.tag:
            return str(self.value)
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, props)
        self.props = props if props else {}
        self.children = children

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is missing")
        if self.children is None:
            raise ValueError("Children are missing")
        #print(f"DEBUG: props = {self.props}")
        return f'<{self.tag}{self.props_to_html()}>' + "".join(f'{i.to_html()}' for i in self.children) + f'</{self.tag}>'