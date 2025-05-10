import spacy
nlp = spacy.load("en_core_web_trf")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
for d in doc:
    print(d.text)