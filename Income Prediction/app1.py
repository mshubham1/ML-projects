from flask import Flask,render_template,request
from log_file.logger import Logs
import pandas as pd
import joblib
import numpy as np
import pymongo
import ssl

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
data=pd.read_csv("data/incomeData.csv")
data=data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
data.replace('?',np.NaN,inplace=True)
columns_with_nan = ['workclass', 'occupation', 'native-country']
for col in columns_with_nan:
    data[col].fillna(data[col].mode()[0], inplace=True)
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
for col in data.columns:
    if data[col].dtypes == 'object':
        data[col] = encoder.fit_transform(data[col])
X=data.drop(['Income'],axis=1)
y=data['Income']
X = X.drop(['workclass', 'education', 'race', 'sex',
            'capital-loss', 'native-country'], axis=1)
X_scaled=scaler.fit_transform(X)

log = Logs("log_file/log_data.log")
log.addLog("INFO", "Execution started Successfully !")

# configuring logging method
pickle_in = open("model_rf.pkl","rb")
model=joblib.load(pickle_in)

app = Flask(__name__)
# route for main page
@app.route('/')
def index():
    return render_template("index.html")

def prediction1(age, fnlwgt, education_num,  marital_status, occupation, relationship, capital_gain, hours_per_week):
    dct_marital_status={'Never-married':4,'Married-civ-spouse':2 ,'Divorced':0, 'Married-spouse-absent':3,
    'Separated':5 ,'Married-AF-spouse':1, 'Widowed':6}
    dct_occupation ={'Adm-clerical':0 ,'Exec-managerial':3 ,'Handlers-cleaners':5 ,'Prof-specialty':9,
     'Other-service':7, 'Sales':11, 'Craft-repair':2, 'Transport-moving':13,
     'Farming-fishing':4, 'Machine-op-inspct':6 ,'Tech-support':12 ,'Protective-serv':10,
     'Armed-Forces':1, 'Priv-house-serv':8}
    dct_relationship= {'Not-in-family':1 ,'Husband':0, 'Wife':5 ,'Own-child':3 ,'Unmarried':4, 'Other-relative':2}
    
    #cols=['age', 'fnlwgt', 'education_num','marital_status', 'occupation','relationship','capital_gain', 'hours_per_week']
    X=[age,fnlwgt,education_num,dct_marital_status[marital_status],dct_occupation[occupation],dct_relationship[relationship],capital_gain,hours_per_week]
    final_features = [np.array(X)]
    print(final_features)
    print(scaler.transform(final_features))
    result = model.predict(scaler.transform(final_features))
    return result
    

# route for prediction 
@app.route('/predict', methods=['POST','GET'])
def predict():
    if request.method == "POST":
        age = request.form.get("age")
        fnlwgt = request.form.get("fnlwgt")
        education_num = request.form.get("education_num")  
        marital_status =request.form.get("marital_status")
        occupation =request.form.get("occupation")
        relationship =request.form.get("relationship")
        capital_gain =request.form.get("capital_gain")
        hours_per_week = request.form.get("hours_per_week")
        log.addLog("INFO", "Successfully retrieved information from the user... !")
        input1=[age, fnlwgt, education_num,  marital_status, occupation, relationship, capital_gain, hours_per_week]
        print(input1)
        print(model)
        result = prediction1(age, fnlwgt, education_num,  marital_status, occupation, relationship, capital_gain, hours_per_week)
        print(result)
        
        #Data Ingestion
        # database connections
        try:
            default_connection_url ="mongodb+srv://mafia123:mafia123@cluster0.j7nj9.mongodb.net/visibility_prediction?retryWrites=true&w=majority"
            client = pymongo.MongoClient(default_connection_url,ssl_cert_reqs=ssl.CERT_NONE)
            print("Database connection established.")
            log.addLog("INFO", "Database connection established..! !")
        except Exception as e:
            log.addLog("ERROR", "Error while connecting to Database :{}".format(e))

        #creation of collection      
        try:
            db_name = "Income_prediction"
            database = client[db_name]
            log.addLog("INFO", "Database Created !")
            print("Collection Created")
            collection_name = "user_data"
            collection = database[collection_name]
            log.addLog("INFO", "Collection Created!")
        except Exception as e:
            log.addLog("ERROR", "Found error in DB or Collection : {}".format(e))
        
        #insertion in collection
        try:
            info = {
                    'age' :age ,
                    'fnlwgt':fnlwgt ,
                    'education_num' :education_num ,
                    'marital_status' :marital_status,
                    'occupation' : occupation ,
                    'relationship':relationship,
                    'capital_gain' : capital_gain ,
                    'hours_per_week' : hours_per_week 
                }
            collection.insert_one(info)
            log.addLog("INFO", "Data Inserted in the Collection Successfully !!")
            client.close()
            log.addLog("INFO", "Database connection closed Successfully !!")
        except Exception as e:
            log.addLog("ERROR", "found error in info json :{}".format(e))
            return render_template('index.html')
        log.addLog("INFO", "Prediction done Successfully !")

        if result == 1:
            output = "Income is more than 50K"
        elif result == 0:
            output = "Income is less than 50K"
        
        return render_template('index.html', prediction_text='{}'.format(output))

    else:
        log.addLog("INFO", "Return from the Predict Route!!")
        return render_template('index.html')
   

@app.route("/database")
def database():
    
    heading = ('age', 'fnlwgt', 'education_num','marital_status', 'occupation','relationship','capital_gain', 'hours_per_week')
    all_data = ""
    try:
        default_connection_url ="mongodb+srv://mafia123:mafia123@cluster0.j7nj9.mongodb.net/visibility_prediction?retryWrites=true&w=majority"
        client = pymongo.MongoClient(default_connection_url,ssl_cert_reqs=ssl.CERT_NONE)
        log.addLog("INFO", "Database connection established..! !")
        database = client["Income_prediction"]
        collection = database["user_data"]
        all_data = collection.find()
        log.addLog("INFO", "Retriviwed all data from Collection user_data !")
        ele=[]
        for data in collection.find():
            ele.append([data['age'],data['fnlwgt'],data['education_num'],data['marital_status'],data['occupation'],data['relationship'],data['capital_gain'],data['hours_per_week']])
        client.close()
        log.addLog("INFO", "Closing the Connection !")

    except Exception as error:
        print("Error occured while fetching all data from Database !", error)
        log.addLog("ERROR", "Error occured while fetching all data from Database : {} !" .format(error))



    log.addLog("INFO", "Rendering tamplate <database.html> with all Data !")
    return render_template('database.html', heading = heading, data = ele)


if __name__ == "__main__":
    #app.run(host='0.0.0.0',port=8080)
    app.run(debug=True)
