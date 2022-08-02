import re

def gpa_parse(text):
    pattern = re.compile(r'''((?<=[\s:\(\[\/\-\~c\\u200c])(?<!(\.org/)|(doi:\s))1?[0-9]\.\d{1,4}\s?(\/\s?1?\d\.?\d{0,4})?)|((?<=GPA[\s:])\d)''', re.IGNORECASE)
    return _match(pattern, text)

def test_score_parse(text):
    #Supports ACT, SAT, LSAT, PSAT, AP, ASVAB, GRE, GMAT
    pattern = re.compile(r'''((?<=\W)ACT\W.{0,10}[1-3]?\d)|([1-3]\d\D{0,10}\WACT(?=\W))|((?<=\W)P?L?SAT\W.{0,10}1?\d{3})|(1?\d{3}\D{0,10}\WP?L?SAT(?=\W))|((?<=\W)GRE\W.{0,10}1?[3-7]\d)|(1?[3-7]\d\D{0,10}\WGRE(?=\W))|((?<=\W)AP\W.{0,10}[1-5])|([1-5]\D{0,10}\WAP(?=\W))|((?<=\W)GMAT\W.{0,10}[2-8]\d{2})|([2-8]\d{2}\D{0,10}\WGMAT(?=\W))|((?<=\W)ASVAB\W.{0,10}1?\d{2})|(1?\d{2}\D{0,10}\WASVAB(?=\W))''')
    return _match(pattern, text)

def _match(pattern, text):
    results = re.finditer(pattern, text)
    return results