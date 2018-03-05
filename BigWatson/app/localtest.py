from NLU import analyzer
from NLU import seqtable

for e in analyzer.analyze("This is a test of the NLU package. The analyzer should return an entity generator."):
    print(e)
