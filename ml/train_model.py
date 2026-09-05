import pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score

df=pd.read_csv("ml/student_performance.csv")
X=df[["attendance","internal","assignment","gpa","failures"]]; y=df["performance"]
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
models={
"Logistic Regression":Pipeline([("scale",StandardScaler()),("clf",LogisticRegression(max_iter=2000))]),
"Decision Tree":DecisionTreeClassifier(max_depth=6,random_state=42),
"Random Forest":RandomForestClassifier(n_estimators=300,random_state=42)
}
out=[]
for name,m in models.items():
    m.fit(Xtr,ytr); p=m.predict(Xte)
    out.append([name,accuracy_score(yte,p),precision_score(yte,p,average="weighted",zero_division=0),
                recall_score(yte,p,average="weighted",zero_division=0),f1_score(yte,p,average="weighted",zero_division=0)])
    if name=="Random Forest": joblib.dump(m,"ml/student_performance_model.pkl")
pd.DataFrame(out,columns=["Model","Accuracy","Precision","Recall","F1"]).to_csv("reports/model_comparison.csv",index=False)
print(pd.DataFrame(out,columns=["Model","Accuracy","Precision","Recall","F1"]))
