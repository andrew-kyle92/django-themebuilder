# A dictionary of HTML elements and their common attributes

class BaseAttributes:
    def __init__(self):
        self.base_attributes = ["id", "class", "title", "style"]

    def get_attributes(self):
        return self.base_attributes


class Attributes(BaseAttributes):
    def __init__(self):
        super().__init__()
        self.elements = {
            "a": {"attributes": ["href", "download", "target", "black"]},
            "article": {"attributes": []},
            "canvas": {"attributes": ["height", "width"]},
            "div": {"attributes": []},
            "footer": {"attributes": []},
            "h1": {"attributes": []},
            "h2": {"attributes": []},
            "h3": {"attributes": []},
            "h4": {"attributes": []},
            "h5": {"attributes": []},
            "h6": {"attributes": []},
            "header": {"attributes": []},
            "img": {"attributes": ["alt", "height", "width", "src"]},
            "li": {"attributes": ["value"]},
            "main": {"attributes": []},
            "nav": {"attributes": []},
            "ol": {"attributes": ["reversed", "start", "type"]},
            "p": {"attributes": []},
            "section": {"attributes": []},
            "svg": {"attributes": []},
        }

    def get_element(self, el):
        element = self.elements[el]
        element["attributes"].extend(self.get_attributes())
        return element
