from xml.etree import ElementTree as ET


class Category:
    """
    How to use
    ----------
    Below, we create a quiz, add 1 category, 
    add 2 questions, add another category and 
    then, add two more questions
    
    quiz = Quiz() # create a quiz
    
    cat1 = Category(name="This is a category") # create a category
    quiz.add_category(cat1) # add the category to the quiz
    
    quiz.add_question(question1) # add a question
    quiz.add_question(question2) # add a question
    
    cat2 = Category(name="This is a category") # create another category
    quiz.add_category(cat2) # add the category to the quiz
    
    quiz.add_question(question3) # add a question
    quiz.add_question(question4) # add a question
    """
    def __init__(self, name: str, info: str='', idnumber: str=''):
        self.name = self._validate_name(name)
        self.info = info # some description in html format
        self.idnumber = idnumber # can be anything

    def _validate_name(self, text: str):
        if len(text) == 0:
            raise ValueError('The name of the category must have at least one letter or digit')
        return text

    def tree(self):

        question = ET.Element('question', type='category')

        category = ET.SubElement(question, 'category')
        ET.SubElement(category, 'text').text = f'$course$/top/{self.name}'

        info = ET.SubElement(question, 'info', format='html')
        ET.SubElement(info, 'text').text = f'<![CDATA[{self.info}]]>'

        ET.SubElement(question, 'idnumber').text = self.idnumber

        return question