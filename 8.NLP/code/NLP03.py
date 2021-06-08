from nltk.tokenize import word_tokenize
import nltk

train = [('i like you', 'pos'),
         ('i hate you', 'neg'),
         ('you like me', 'neg'),
         ('i like her', 'pos')]

all_words = set(word.lower() for sentence in train for word in word_tokenize(sentence[0]))
t = [({word:(word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in train]

classifier = nltk.NaiveBayesClassifier.train(t)
#classifier.show_most_informative_features()

test = "i like MeRui"
test_sent_feature = {word.lower(): (word in word_tokenize(test.lower())) for word in all_words}
#print(classifier.classify(test_sent_feature))


from konlpy.tag import  Okt

pos_tagger = Okt()

train = [("메리가 좋아","pos"),
         ("고양이도 좋아","pos"),
         ("난 수업이 지루해","neg"),
         ("메리는 이쁜 고양이","pos"),
         ("너는 못생겼어","neg")]

all_words = set(word.lower() for sentence in train for word in word_tokenize(sentence[0]))
t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in train]

classifier = nltk.NaiveBayesClassifier.train(t)
#classifier.show_most_informative_features()

test = "난 메리가 너무 좋아"
test_sent_feature = {word.lower(): (word in word_tokenize(test.lower())) for word in all_words}
#print(classifier.classify(test_sent_feature))
