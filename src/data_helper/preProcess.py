from nltk.tokenize import sent_tokenize,word_tokenize
import nltk

sentence="E and cdk2  bbbbb2 kinase eeeee2  activities"
print(sentence)

word=word_tokenize(sentence,language='english')
print("{0}".format(' '.join(word)))