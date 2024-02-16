import nltk
from nltk.corpus import brown
train_sents = brown.tagged_sents()
unigram_tagger = nltk.UnigramTagger(train_sents)
tokens=nltk.word_tokenize("move to the north")
tagged=unigram_tagger.tag(tokens)
print(tagged)