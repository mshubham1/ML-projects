import numpy as np
import pickle
import pandas as pd
import streamlit as st 
from PIL import Image


#classifier=Booster.save_model('XGBRegressor.pkl')
pickle_in = open("Random.pkl","rb")
classifier=pickle.load(pickle_in)

st.title('Income Prediction using Machine Learning')
#@app.route('/')
def welcome():
    return "Welcome All"

#@app.route('/predict',methods=["Get"])
def predict(age, fnlwgt, education_num, hours_per_week, workclass, marital_status, occupation, relationship, race, sex, native_country):
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
    prediction = classifier.predict(test_row)
    print(prediction)
    return prediction



def main():
      html_temp = """
      <div style="background-color:green;padding:10px">
      <h2 style="color:white;text-align:center;">Income Prediction</h2>
      </div>
      """
      df = pd.DataFrame({'workclass': ['State-gov', 'Self-emp-not-inc' ,'Private', 'Federal-gov' ,'Local-gov',
 'Self-emp-inc', 'Without-pay' ,'Never-worked'],
                   'marital_status': ['Never-married' ,'Married-civ-spouse' ,'Divorced' ,'Married-spouse-absent',
 'Separated', 'Married-AF-spouse', 'Widowed'],
                   'occupation': ['Adm-clerical' ,'Exec-managerial', 'Handlers-cleaners' ,'Prof-specialty',
 'Other-service' ,'Sales' ,'Craft-repair' ,'Transport-moving',
 'Farming-fishing' ,'Machine-op-inspct' ,'Tech-support' ,'Protective-serv',
 'Armed-Forces' ,'Priv-house-serv'],
                    'relationship':['Not-in-family', 'Husband', 'Wife' ,'Own-child' ,'Unmarried', 'Other-relative'],
                     'race':['White' ,'Black', 'Asian-Pac-Islander' ,'Amer-Indian-Eskimo', 'Other'],
                     'sex':['Male', 'Female'] ,
                     'native_country':['United-States' ,'Cuba', 'Jamaica', 'India', 'Mexico', 'South', 'Puerto-Rico',
     'Honduras', 'England', 'Canada', 'Germany', 'Iran', 'Philippines', 'Italy',
     'Poland', 'Columbia', 'Cambodia','Thailand', 'Ecuador' ,'Laos','Taiwan',
     'Haiti', 'Portugal', 'Dominican-Republic', 'El-Salvador', 'France',
     'Guatemala', 'China', 'Japan','Yugoslavia', 'Peru',
     'Outlying-US(Guam-USVI-etc)', 'Scotland', 'Trinadad&Tobago','Greece',                 
     'Nicaragua', 'Vietnam', 'Hong', 'Ireland', 'Hungary', 'Holand-Netherlands']})
    
      st.markdown(html_temp,unsafe_allow_html=True)
      age = st.text_input("age","eg.35")
      fnlwgt = st.text_input("fnlwgt","eg. 40")
      education_num = st.text_input("education_num","eg. 45")
      hours_per_week = st.text_input("hours-per-week","eg. 41")
      hosp_list = st.sidebar.selectbox("Select Hospital", df["native_country"].unique())
      workclass = st.text_input("workclass","eg. 60")
      marital_status = st.text_input("marital_status","eg. 60")
      occupation = st.text_input("occupation","eg. 60")
      relationship = st.text_input("relationship","eg. 60")
      race = st.text_input("race","eg. 60")
      sex = st.text_input("sex","eg. 60")
      native_country = st.text_input("native_country","eg. 60")
      result=""
      if st.button("Predict"):
          result=predict(age, fnlwgt, education_num, hours_per_week, workclass, marital_status, occupation, relationship, race, sex, native_country)
      if result==0:
          st.success('The  Income is:  {}'.format('<=50K'))
      else:
          st.success('The Income is {}'.format('>50K'))

if __name__=='__main__':
    main()
  