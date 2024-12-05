# This file is specifically for handling all html elements
from .elements import Attributes


class HtmlElement(Attributes):
    def __init__(self):
        super().__init__()

    def get_element(self, element):
        return super(HtmlElement, self).get_element(element)
