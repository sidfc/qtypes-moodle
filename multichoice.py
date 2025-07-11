from xml.etree import ElementTree as ET

from question import Question
from utils import bool2str


# Fraction used by the q_type MultipleChoice from Moodle
FRACTIONS = {
    0.0: "0", 
    # positives
    1.0: "100", 
    0.9: "90", 
    5/6: "83.33333", 
    0.8: "80", 
    3/4: "75", 
    0.7: "70", 
    2/3: "66.66667", 
    0.6: "60", 
    0.5: "50", 
    0.4: "40", 
    1/3: "33.33333", 
    0.3: "30", 
    1/4: "25", 
    0.2: "20", 
    1/6: "16.66667", 
    1/7: "14.28571", 
    1/8: "12.5", 
    1/9: "11.11111", 
    0.1: "10", 
    0.05: "5",
    # negatives
    -1.0: "-100", 
    -0.9: "-90", 
    -5/6: "-83.33333", 
    -0.8: "-80", 
    -3/4: "-75", 
    -0.7: "-70", 
    -2/3: "-66.66667", 
    -0.6: "-60", 
    -0.5: "-50", 
    -0.4: "-40", 
    -1/3: "-33.33333", 
    -0.3: "-30", 
    -1/4: "-25", 
    -0.2: "-20", 
    -1/6: "-16.66667", 
    -1/7: "-14.28571", 
    -1/8: "-12.5", 
    -1/9: "-11.11111", 
    -0.1: "-10", 
    -0.05: "-5"
}


class Answer:
    """
    TODO - document this
    """
    def __init__(self, text: str, fraction: str, feedback: str=''):
        self.text = text
        self.fraction = fraction
        self.feedback = feedback

    def tree(self):

        element = ET.Element('answer', fraction=self.fraction, format='html')
        ET.SubElement(element, 'text').text = f'<![CDATA[{self.text}]]>'

        feedback = ET.SubElement(element, 'feedback', format='html')
        ET.SubElement(feedback, 'text').text = f'<![CDATA[{self.feedback}]]>'
        
        return element


class Hint:
    """
    TODO - document this
    """
    def __init__(self, text: str, shownumcorrect: bool=False, clearwrong: bool=False):
        self.text = text
        self.shownumcorrect = shownumcorrect
        self.clearwrong = clearwrong

    def tree(self):

        element = ET.Element('hint', format="html")
        ET.SubElement(element, 'text').text = f'<![CDATA[{self.text}]]>'

        if self.shownumcorrect is True:
            ET.SubElement(element, 'shownumcorrect')

        if self.clearwrong is True:
            ET.SubElement(element, 'clearwrong')
        
        return element


class MultiChoice(Question):
    """
    Parameters
    ----------
    answernumbering: 'abc', 'ABCD', '123', 'iii', 'IIII', 'none'
    """
    def __init__(self, name: str, questiontext: str, single: bool=True, shuffleanswers: bool=True, answernumbering: str='abc', *args, **kwargs):
        super().__init__(name, questiontext, *args, **kwargs)
        self.type = 'multichoice'
        self.single = single
        self.shuffleanswers = shuffleanswers
        self.answernumbering = answernumbering
        self.showstandardinstruction: bool = False
        self.correctfeedback: str = 'Sua resposta está correta.'
        self.partiallycorrectfeedback: str = 'Sua resposta está parcialmente correta.'
        self.incorrectfeedback: str = 'Sua resposta está incorreta.'
        self.answers = []
        self.hints = []
        self.fractions = []

    def tree(self):
        
        self._are_fractions_valid()

        question = super().tree()

        ET.SubElement(question, 'single').text = bool2str(self.single)
        ET.SubElement(question, 'shuffleanswers').text = bool2str(self.shuffleanswers)
        ET.SubElement(question, 'answernumbering').text = self.answernumbering
        ET.SubElement(question, 'showstandardinstruction').text = bool2str(self.showstandardinstruction)

        for item in ['correctfeedback', 'partiallycorrectfeedback', 'incorrectfeedback']:
            el = ET.SubElement(question, item)
            ET.SubElement(el, 'text').text = f'<![CDATA[{getattr(self, item)}]]>'

        if len(self.answers) == 0:
            raise ValueError('There are no answers for this question')
        
        for answer in self.answers:
            question.append(answer)

        for hint in self.hints:
            question.append(hint)

        self._add_tags_to_root(question)

        return question

    def add_answer(self, text, fraction, feedback=''):
        answer = Answer(text, FRACTIONS[fraction], feedback)
        self.fractions.append(float(answer.fraction))
        self.answers.append(answer.tree())

    def add_hint(self, text, **kwargs):
        hint = Hint(text, **kwargs).tree()
        self.hints.append(hint)

    def _are_fractions_valid(self):
        s = sum(fi for fi in self.fractions if fi > 0)
        if self.single is False and round(s, 3) != 100:
            raise ValueError(f'As notas positivas que você escolheu não somam 100%\nAo invés disso, elas somam {s}%')
        if self.single is True and 100 not in self.fractions:
            raise ValueError('Uma das opções deve ser 100% para que seja possível conseguir uma nota máxima nessa questão.')


if __name__ == '__main__':

    from moodle_qtypes.quiz import Quiz
    from moodle_qtypes.category import Category
    from moodle_qtypes.utils import xml_to_str

    quiz = Quiz()

    cat = Category('category_name')
    quiz.add(cat)#, info='questions related to addition, just a basic arithmetic operation')

    q = MultiChoice('Name of the question', 'Quanto é 2 + 2?')
    q.add_tags(['tag1', 'tag2'])
    q.add_answer('8', 0.3)
    q.add_answer('4', 1)
    q.add_answer('1', -0.2)
    q.add_tags(['tag3', 'tag4'])
    q.add_answer('-2', 0.5)
    q.add_answer('-6', 0.2)
    q.add_answer('-8', 0)
    q.add_hint('Try this 1', shownumcorrect=True, clearwrong=True)
    q.add_hint('Try this 2')
    q.add_hint('Try this 3', shownumcorrect=False, clearwrong=True)

    quiz.add(q)

    print(xml_to_str(quiz.tree()))
    # quiz.save('file.xml')