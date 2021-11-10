from flask import Flask,render_template,request
from log_file.logger import Logs
import pandas as pd
import pickle
import numpy as np
import pymongo
import ssl


log = Logs("log_file/log_data.log")
log.addLog("INFO", "Execution started Successfully !")

# configuring logging method
pickle_in = open("Random.pkl","rb")
model=pickle.load(pickle_in)

app = Flask(__name__)
# route for main page
@app.route('/')
def index():
    return render_template("index.html")

def prediction1(age, fnlwgt, education_num, hours_per_week, workclass, marital_status, occupation, relationship, race, sex, native_country):
    dct_workclass={'State-gov':6,'Self-emp-not-inc':5,'Private':3,'Federal-gov':0, 'Local-gov':1,
    'Self-emp-inc': 4,'Without-pay':7,'Never-worked':2 }
    dct_marital_status={'Never-married':4,'Married-civ-spouse':2 ,'Divorced':0, 'Married-spouse-absent':3,
    'Separated':5 ,'Married-AF-spouse':1, 'Widowed':6}
    dct_occupation ={'Adm-clerical':0 ,'Exec-managerial':3 ,'Handlers-cleaners':5 ,'Prof-specialty':9,
     'Other-service':7, 'Sales':11, 'Craft-repair':2, 'Transport-moving':13,
     'Farming-fishing':4, 'Machine-op-inspct':6 ,'Tech-support':12 ,'Protective-serv':10,
     'Armed-Forces':1, 'Priv-house-serv':8}
    dct_relationship= {'Not-in-family':1 ,'Husband':0, 'Wife':5 ,'Own-child':3 ,'Unmarried':4, 'Other-relative':2}
    dct_native_country ={'United-States':38, 'Cuba':4, 'Jamaica':22, 'India':18, 'Mexico':25, 'South':34, 'Puerto-Rico':32,
     'Honduras':15, 'England':8, 'Canada':1, 'Germany':10, 'Iran':19, 'Philippines':29, 'Italy':21,
     'Poland':30, 'Columbia':3, 'Cambodia':0 ,'Thailand':36, 'Ecuador':6 ,'Laos':24 ,'Taiwan':35,
     'Haiti':13, 'Portugal':31, 'Dominican-Republic':5, 'El-Salvador':7, 'France':9,
     'Guatemala':12, 'China':2, 'Japan':23 ,'Yugoslavia':40, 'Peru':28,
     'Outlying-US(Guam-USVI-etc)':27, 'Scotland':33, 'Trinadad&Tobago':37,'Greece':11,                 
     'Nicaragua':26, 'Vietnam':39, 'Hong':16, 'Ireland':20, 'Hungary':17, 'Holand-Netherlands':14}
    dct_race={'White':4, 'Black':2, 'Asian-Pac-Islander':1, 'Amer-Indian-Eskimo':0 ,'Other':3}
    dct_sex={'Male':1,'Female':0}
    
    cols=['age', 'fnlwgt', 'education_num', 'hours_per_week', 'workclass', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'native_country']
    X=[0 for i in range(1,12)]
    X[1]=age
    X[2]=fnlwgt
    X[3]=education_num
    X[4]=hours_per_week
    X[5]=dct_workclass[workclass]
    X[6]=dct_marital_status[marital_status]
    X[7]=dct_occupation[occupation]
    X[8]=dct_relationship[relationship]
    X[9]=dct_race[race]
    X[10]=dct_sex[sex]
    X[11]=dct_native_country[native_country]
    test_row = pd.DataFrame(X).transpose()
    test_row.columns = cols
    result = model.predict(test_row)
    print(result)
    return result


# route for prediction 
@app.route('/predict', methods=['POST','GET'])
def predict():
    if request.method == "POST":
        age = request.form.get("age")
        fnlwgt = request.form.get("fnlwgt")
        education_num = request.form.get("education_num")
        hours_per_week = request.form.get("hours_per_week")
        
        workclass = request.form.get("workclass")
        marital_status =request.form.get("marital_status")
        occupation =request.form.get("occupation")
        relationship =request.form.get("relationship")
        race =request.form.get("race")
        sex =request.form.get("sex")
        native_country =request.form.get("native_country")
        log.addLog("INFO", "Successfully retrieved information from the user... !")
        input1=[age, fnlwgt, education_num, hours_per_week, workclass, marital_status, occupation, relationship, race, sex, native_country]
        print(input1)
        print(model)
        result = prediction1(input1)
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
                    'hours_per_week' : hours_per_week ,
                    'workclass' : workclass,
                    'marital_status' :marital_status,
                    'occupation' : occupation ,
                    'relationship':relationship,
                    'race': race,
                    'sex': sex,
                    'native_country' : native_country 
                }
            collection.insert_one(info)
            log.addLog("INFO", "Data Inserted in the Collection Successfully !!")
            client.close()
            log.addLog("INFO", "Database connection closed Successfully !!")
        except Exception as e:
            log.addLog("ERROR", "found error in info json :{}".format(e))
            return render_template('index.html')
        log.addLog("INFO", "Prediction done Successfully !")
        if result==0:
            return render_template('index.html',result="the Income is : '<=50K'")
        else:
            return render_template('index.html',result="the Income is : '>50K'")

    else:
        log.addLog("INFO", "Return from the Predict Route!!")
        return render_template('index.html')
   

@app.route("/database")
def database():
    
    heading = ('age', 'fnlwgt', 'education_num', 'hours_per_week', 'workclass', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'native_country')
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
            ele.append([data['age'],data['fnlwgt'],data['education_num'],data['hours_per_week'],data['workclass'],data['marital_status'],data['occupation'],data['relationship'],data['race'],data['sex'],data['native_country']])
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
