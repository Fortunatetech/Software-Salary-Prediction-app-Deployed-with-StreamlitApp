import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_trained_model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
label_encoder_Country = data["label_encoder_Country"]
label_encoder_Education = data["label_encoder_Education"]


def show_predict_page():
    st.title("Salary Prediction App for Software Developers")

    st.write("""### Put in some information to predict the salary""")

    countries = (
       'United Kingdom of Great Britain and Northern Ireland',
       'Netherlands',
       'United States of America',
       'Austria',
       'Italy',
       'Canada',
       'Germany',
       'Poland',
       'France',
       'Brazil',
       'Sweden',
       'Spain',
       'Turkey',
       'India',
       'Russian Federation',
       'Switzerland',
       'Australia'
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)

    expericence = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Predict Salary")
    if ok:
        X_train = np.array([[country, education, expericence ]])
        X_train[:, 1] = label_encoder_Country.transform(X_train[:,1])
        X_train[:, 0] = label_encoder_Education.transform(X_train[:,0])
        X_train = X_train.astype(float)

        salary = regressor.predict(X_train)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")



