import html
from xml.etree import ElementTree as ET

from utils import xml_to_str


class Question:
    """
    TODO - document this
    """
    def __init__(self, name: str, questiontext: str, *args, **kwargs):
        self.name: str = name
        self.questiontext: str = questiontext
        self.type: str = 'parent'
        self.generalfeedback: str = ''
        self.defaultgrade: float = 1.0
        self.penalty: bool = 0
        self.hidden: bool = 0
        self.idnumber: str = ''
        self.tags: str = []

    def tree(self):
        question = ET.Element('question', type=self.type)

        name = ET.SubElement(question, 'name')
        ET.SubElement(name, 'text').text = self.name

        questiontext = ET.SubElement(question, 'questiontext', format='html')
        ET.SubElement(questiontext, 'text').text = f'<![CDATA[{self.questiontext}]]>'

        generalfeedback = ET.SubElement(question, 'generalfeedback', format='html')
        ET.SubElement(generalfeedback, 'text').text = f'<![CDATA[{self.generalfeedback}]]>'

        ET.SubElement(question, 'defaultgrade').text = str(self.defaultgrade)

        ET.SubElement(question, 'penalty').text = str(self.penalty)

        ET.SubElement(question, 'hidden').text = str(self.hidden)

        ET.SubElement(question, 'idnumber').text = self.idnumber

        return question

    def add_tags(self, tag_list: list[str]):
        self.tags.extend(tag_list)

    def _add_tags_to_root(self, root):
        """
        This method is here to put the tags
        at the end of the question xml tree
        """
        tags = ET.SubElement(root, 'tags')
        for text in self.tags:
            tag = ET.SubElement(tags, 'tag')
            ET.SubElement(tag, 'text').text = text

    def to_str(self):
        return xml_to_str(self.tree())