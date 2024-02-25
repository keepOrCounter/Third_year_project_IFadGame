import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.tag.hunpos import HunposTagger
from os.path import expanduser

home = expanduser("~")
_path_to_bin = home + '\\hunpos-1.0-win\\hunpos-tag.exe'
_path_to_model = home + '\\hunpos-1.0-win\\english.model'
ht = HunposTagger(path_to_model=_path_to_model, path_to_bin=_path_to_bin)

def get_word_meaning_in_phrase(phrase, word):
    tokens = word_tokenize(phrase)
    tagged_tokens = ht.tag(phrase.split())
    ht.close()

    # 找到目标单词在短语中的词性标签
    word_pos = None
    for token, pos in tagged_tokens:
        if token.lower() == word.lower():
            word_pos = pos
            break
    
    print(tagged_tokens)

    if word_pos:
        # 根据词性标签在WordNet中找到对应的含义
        word_pos = str(word_pos, 'utf-8')
        synsets = wordnet.synsets(word, pos=word_pos[0].lower())
        if synsets:
            # 获取短语中其他单词的同义词集合
            other_words_synsets = []
            for token, pos in tagged_tokens:
                if token.lower() != word.lower():
                    pos = str(pos, 'utf-8')
                    synsets2 = wordnet.synsets(token, pos=pos[0].lower())
                    other_words_synsets.extend(synsets2)
            
            meanings = [synset.definition() for synset in synsets]
            return meanings, synsets, other_words_synsets
        else:
            return None, None, None
    else:
        return None, None, None

# 示例短语和目标单词
phrase = "move to the north"
def verbFinder(text):
    tagged_tokens = ht.tag(text.split())
    for token, pos in tagged_tokens:
        pos = str(pos, 'utf-8')
        if pos[0].lower() == 'v':
            return token
word = verbFinder(phrase)
synonymsList = []

# 获取目标单词在短语中的意思和相应的同义词集合
meanings, synsets, other_words_synsets = get_word_meaning_in_phrase(phrase, word)
if meanings:
    # 显示与给定含义相关的同义词集合
    for synset in synsets:
        for lemma in synset.lemmas():
            synonymsList.append(lemma.name())
    print(f"\nSynonyms for '{word}':")
    synonymsList = list(dict.fromkeys(synonymsList))
    print(synonymsList)
 
    # # 显示短语中其他单词的同义词集合
    # print("\nOther words' synonyms in the context of the phrase:")
    # for other_word_synsets in other_words_synsets:
    #     for lemma in other_word_synsets.lemmas():
    #         print(lemma.name())
else:
    print(f"No meanings found for '{word}' in the context of the phrase")

# import nltk
# import sys
# from os.path import expanduser
# home = expanduser("~")
# from nltk.tag.hunpos import HunposTagger
# _path_to_bin = home + '\\hunpos-1.0-win\\hunpos-tag.exe'
# _path_to_model = home + '\\hunpos-1.0-win\\english.model'
# ht = HunposTagger(path_to_model=_path_to_model, path_to_bin=_path_to_bin)
# text = "I move forward"
# def verbFinder(text):
#     tagged_tokens = ht.tag(text.split())
#     for token, pos in tagged_tokens:
#         pos = str(pos, 'utf-8')
#         if pos[0].lower() == 'v':
#             return token
# print(verbFinder(text))
# ht.close()