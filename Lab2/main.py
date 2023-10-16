# Lab 2 - DL4NLP
# @Author: Diana Mocanu
# @Date: 12.10.2023
import spacy
from spacy.lang.en import English

sentences = [
    "The chicken is ready to eat.",
    "John saw the chicken in the street.",
    "The old chicken and ducks eat.",
    "Join is an old ducks enthusiast."
]

## 1. Write a suitable constituency grammar, able to correctly parse all sentences, with all
## their senses. Use as inspiration the grammars discussed in class.


## 2. Use existing modules to extract phrase structure trees for these sentences

## 3. Implement a dependency parser (using, for instance, spaCY, NLTK or Stanza) and
## parse the three sentences above.
nlp = spacy.load('en_core_web_sm')
for sentence in sentences:
    doc = nlp(sentence)
    print(sentence)
    for token in doc:
        print(f"{token.text} --{token.dep_}--> {token.head.text}")
    print("\n")
