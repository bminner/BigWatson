from NLU import analyzer
from NLU import seqtable
from logic import nlu_censor_manager as nlu

text = "The president is a ball gargling idiot."
good_class = 'positive'
sentences = nlu.censor_body(text,good_class)
for sentence in sentences:
    print(sentence)