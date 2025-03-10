import streamlit as st
import joblib
import numpy as np

# Load your trained model
model = joblib.load("loan_model.pkl")  # Ensure you save your trained model as loan_model.pkl

# Load custom CSS
def load_css():
    with open("styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load HTML template
def load_html():
    with open("index.html", "r") as f:
        return f.read()

# Streamlit UI
def main():
    st.set_page_config(page_title="Loan Approval Prediction", layout="centered")
    load_css()

    st.markdown(load_html(), unsafe_allow_html=True)

    # Input Fields
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Married", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    income = st.number_input("Applicant Income", min_value=0)
    co_income = st.number_input("Co-Applicant Income", min_value=0)
    loan_amount = st.number_input("Loan Amount", min_value=0)
    loan_term = st.selectbox("Loan Term (Months)", [12, 36, 60, 120, 180, 240, 300, 360])
    credit_history = st.selectbox("Credit History", [0, 1])
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

    # Convert categorical variables to numerical
    gender = 1 if gender == "Male" else 0
    married = 1 if married == "Yes" else 0
    dependents = int(dependents.replace("+", ""))
    education = 1 if education == "Graduate" else 0
    self_employed = 1 if self_employed == "Yes" else 0
    property_area = {"Urban": 2, "Semiurban": 1, "Rural": 0}[property_area]

    # Prediction
    if st.button("Predict Loan Approval"):
        input_data = np.array([[gender, married, dependents, education, self_employed, 
                                income, co_income, loan_amount, loan_term, credit_history, property_area]])
        prediction = model.predict(input_data)
        
        if prediction[0] == 1:
            st.success("Congratulations! Your loan is approved. 🎉")
        else:
            st.error("Sorry, your loan application is not approved.")

if __name__ == "__main__":
    main()
