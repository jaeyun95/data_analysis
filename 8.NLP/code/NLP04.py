from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(min_df = 1)

contents = ['메리랑 놀러가고 싶지만 바쁜데 어떻하죠?',
            '메리는 공원에서 산책하고 노는 것을 싫어해요',
            '메리는 공원에서 노는 것도 싫어해요. 이상해요.',
            '먼 곳으로 여행을 떠나고 싶은데 너무 바빠서 그러질 못하고 있어요']

t = Okt()
contents_token = [t.morphs(row) for row in contents]

contents_for_vectorize = []

for content in contents_token:
    sentence = ""
    for word in content:
        sentence = sentence + " " + word
    contents_for_vectorize.append(sentence)

X = vectorizer.fit_transform(contents_for_vectorize)
vectorizer.get_feature_names()
num_samples, num_features = X.shape
X.toarray().transpose()

new_post = ["메리랑 공원에서 산책하고 놀고 싶어요"]
new_post_vec = vectorizer.transform(new_post)
new_post_vec.toarray()

import scipy as sp

def dist_raw(v1, v2):
    delta = v1 - v2
    return sp.linalg.norm(delta.toarray())


best_doc = None
best_dist = 65535
best_i = None

for i in range(0, num_samples):
    post_vec = X.getrow(i)
    d = dist_raw(post_vec, new_post_vec)
    print("== Post %i with dist=%.2f   : %s" % (i, d, contents[i]))
    if d < best_dist:
        best_dist = d
        best_i = i

#print("Best post is %i, dist = %.2f" % (best_i, best_dist))
#print('-->', new_post)
#print('---->', contents[best_i])

def tfidf(t, d, D):
    tf = float(d.count(t)) / sum(d.count(w) for w in set(d))
    idf = sp.log(float(len(D))/len([doc for doc in D if t in doc]))
    return tf, idf

a, abb, abc = ["a"],["a","b","b"],["a","b","c"]
D = [a,abb,abc]

'''
print(tfidf('a',a,D))
print(tfidf('b',abb,D))
print(tfidf('a',abc,D))
print(tfidf('b',abc,D))
print(tfidf('c',abc,D))
'''

from sklearn.feature_extraction.text import TfidfVectorizer

contents_token = [t.morphs(row) for row in contents]

contents_for_vectorize = []

for content in contents_token:
    sentence = ""
    for word in content:
        sentence = sentence + " " + word
    contents_for_vectorize.append(sentence)

X = vectorizer.fit_transform(contents_for_vectorize)
num_samples, num_features = X.shape

new_post = ["메리랑 너무 놀고싶다."]
new_post_tokens = [t.morphs(row) for row in new_post]

new_post_for_vectorize = []

for content in new_post_tokens:
    sentence = ""
    for word in content:
        sentence = sentence + " " + word
    new_post_for_vectorize.append(sentence)

new_post_vec = vectorizer.transform(new_post_for_vectorize)

best_doc = None
best_dist = 65535
best_i = None

for i in range(0, num_samples):
    post_vec = X.getrow(i)
    d = dist_raw(post_vec, new_post_vec)
    print("== Post %i with dist=%.2f   : %s" % (i, d, contents[i]))
    if d < best_dist:
        best_dist = d
        best_i = i

print("Best post is %i, dist = %.2f" % (best_i, best_dist))
print('-->', new_post)
print('---->', contents[best_i])