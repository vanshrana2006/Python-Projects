from sklearn.datasets import  load_iris
iris = load_iris()
x = iris.data
y = iris.target
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test= train_test_split(x,y,test_size=0.2)
from sklearn.linear_model import LogisticRegression
model =  LogisticRegression()
model.fit(x_train,y_train)
accuracy = model.score(x_test, y_test)
print(f"Accuracy: {accuracy:.2f}")