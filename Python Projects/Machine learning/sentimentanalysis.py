import pandas as pd
import nltk
from nltk.corpus import movie_reviews
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import random

nltk.download('movie_reviews')

documents = [(movie_reviews.words(fileid), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

data = pd.DataFrame(documents, columns=['review', 'sentiment'])
data['review'] = data['review'].apply(lambda x: ' '.join(x))

X = data['review']
y = data['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_vectorized, y_train)

y_pred = model.predict(X_test_vectorized)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

def predict_sentiment(review):
    review_vectorized = vectorizer.transform([review])
    prediction = model.predict(review_vectorized)
    return prediction[0]

print(predict_sentiment("This movie was fantastic!"))
print(predict_sentiment("I did not like this movie at all."))
