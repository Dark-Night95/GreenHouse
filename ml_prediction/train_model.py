import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import joblib


df = pd.read_csv("prepared_dataset.csv")

print(df.head())
x =df[["Temperature","Humidity","Light"]]
y = df["water_required"]

print("X:")
print(x.head())

print("y:")
print(y.head())

#from here sk_learn starts
x_train,x_test,y_train,y_test =train_test_split(x,y,test_size=0.2,random_state=12)

print("Training data:", len(x_train))
print("Testing data:", len(x_test))


model = RandomForestClassifier(
 n_estimators=100,  #create 100 decision_tree
random_state=12    #same data will randomly split every time
)
model.fit(x_train,y_train) #model will train using data of x and y

joblib.dump(model,"model.pkl")
print("Model saved successfully")

predictions = model.predict(x_test)

accuracy=accuracy_score(y_test,predictions)
print("Accuracy:\n",accuracy)

classification=classification_report(y_test,predictions)
print("Classification Report:\n",classification)

