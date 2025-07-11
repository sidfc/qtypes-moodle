import html
from xml.etree import ElementTree as ET

from utils import xml_to_str


class Quiz:
    """
    TODO - document this
    """
    def __init__(self):
        self.questions = [] # questions or categories

    def tree(self):
        if len(self.questions) == 0:
            raise ValueError('There are no questions in this quiz')

        quiz = ET.Element('quiz')

        for question in self.questions:
            quiz.append(question.tree())

        return quiz

    def add(self, element):
        """
        element can be an instance of Cloze, TrueFalse, MultiChoice, ... or Category
        """
        self.questions.append(element)

    def save(self, dst: str):
        quiz = self.tree()
        ET.indent(quiz, space='\t', level=0)
        quiz = ET.tostring(quiz, encoding='unicode', method='xml')        
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(html.unescape(quiz))

    def to_str(self):
        return xml_to_str(self.tree())