import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load your saved model and scaler
model = joblib.load('v_clf_model.pkl')
scaler = joblib.load('scalar.pkl')


def scale_input(input_data, scaler):
    return scaler.transform(input_data)

def make_prediction(scaled_data, model):
    return model.predict(scaled_data)


lowest_Annual_Income_Threshold = 350000
highest_Annual_Income_Threshold = 2400000
    
lowest_Number_of_Bank_Accounts_Threshold = 5
highest_Number_of_Bank_Accounts_Threshold = 8

lowest_Number_of_Credit_cards_Threshold = 5
highest_Number_of_Credit_cards_Theshold = 7

lowest_Interest_Rate_Threshold = 30
highest_Interest_Rate_Threshold = 50

lowest_Number_of_Loans_Threshold = 2
highest_Number_of_Loans_Threshold = 5

lowest_Delay_from_due_date_Threshold = 15
highest_Delay_from_due_date_Threshold = 50
    
lowest_Number_of_Loans_Threshold = 3
highest_Number_of_Loans_Threshold = 5

lowest_Number_of_Delayed_Payments_Threshold = 3
highest_Number_of_Delayed_Payments_Threshold = 5

lowest_Credit_Utilization_Ration_Threshold = 30
highest_Credit_Utilization_Ration_Threshold = 70

def getGood(prediction, age, ai, ncc, nol, dfd, ndp, cur):
    if( prediction != 2):
        if(age < 30 and ai>350000 and ncc<6 and dfd <=1 and cur<=30 and nol<4 and ndp<=2):
            return 2
    return prediction

def scale_input(input_data, scaler):
    return scaler.transform(input_data)

def make_prediction(scaled_data, model):
    return model.predict(scaled_data)

def getSuggestions(Annual_Income, Number_of_Bank_Accounts, Number_of_Credit_cards, Interest_Rate,
                  Number_of_Loans, Delay_from_due_date, Number_of_Delayed_Payments,
                    Credit_Utilization_Ration):
    
    Suggestions_List=[]

    #Bank Accounts
    if( Number_of_Bank_Accounts >= lowest_Number_of_Bank_Accounts_Threshold ):
        Suggestions_List.append('Please close your Unused Bank Accounts')
        

    #Credit Cards    
    if( Annual_Income < lowest_Annual_Income_Threshold and
        Number_of_Credit_cards >= lowest_Number_of_Credit_cards_Threshold ):
        Suggestions_List.append('Provide the Salary slips and Close new Credit cards') 

    elif( Number_of_Credit_cards >= lowest_Number_of_Credit_cards_Threshold ):
        Suggestions_List.append('Please close your unused new credit cards, to increase the cibil')
        
        
    #Interest Rate
    if( Annual_Income < lowest_Annual_Income_Threshold and
        Interest_Rate > lowest_Interest_Rate_Threshold ):
        Suggestions_List.append('As you Annual Income is very low, So to avoid higher intrest rates avoid late payments')
        

    #Number of Loans    
    if( Annual_Income < lowest_Annual_Income_Threshold and 
        Number_of_Loans > lowest_Number_of_Loans_Threshold ):
        Suggestions_List.append('As your Income is low, Clear your loans which have minimum loan amount')

    elif( Annual_Income >= lowest_Annual_Income_Threshold and
        Annual_Income < highest_Annual_Income_Threshold and
        Number_of_Loans > lowest_Number_of_Loans_Threshold ):
        Suggestions_List.append('To Increase the cibil , Clear your lowest loan amounts')

    elif(Number_of_Loans > lowest_Number_of_Loans_Threshold and
       Number_of_Loans < highest_Number_of_Loans_Threshold ):
        Suggestions_List.append('As you have many loans clear the loans to create positive impact in your in cibil')

    elif(Number_of_Loans > highest_Number_of_Loans_Threshold ):
        Suggestions_List.append('Number of Loans are Too High 😅, which will create negitive impact in cibil so clear minimum loans')

    #Delay
    if( Number_of_Delayed_Payments == 0 and Delay_from_due_date == 0):
        Suggestions_List.append('Your payments are on time 👍 so maintain this to increase your cibil')

    if ((Delay_from_due_date > lowest_Delay_from_due_date_Threshold  and
        Delay_from_due_date < highest_Delay_from_due_date_Threshold ) or
        (Number_of_Delayed_Payments >= lowest_Number_of_Delayed_Payments_Threshold and
        Number_of_Delayed_Payments < highest_Number_of_Delayed_Payments_Threshold)):
        Suggestions_List.append('Your are delaying the payments, Please Try to do the payments without delaying')

        
    #Delay from due date
    if( Delay_from_due_date > 0 and Delay_from_due_date < lowest_Delay_from_due_date_Threshold ):
        Suggestions_List.append('Even Though Your delayed days are less, But it is not good')

    if( Number_of_Delayed_Payments >= highest_Number_of_Delayed_Payments_Threshold ):
        Suggestions_List.append('Your Delayed Payments are too High, Pay before its becoming too late')
    

    #Number of Delayed Payments
    if( Number_of_Delayed_Payments > 0 and Number_of_Delayed_Payments < lowest_Number_of_Delayed_Payments_Threshold ):
        Suggestions_List.append('Even Thought Your delayed payments are less, But it is not good')

    if( Number_of_Delayed_Payments >= highest_Number_of_Delayed_Payments_Threshold ):
        Suggestions_List.append('Your Delayed Days are too High, Pay before its becoming too late')

        
    #Utilization Ratio
    if( Credit_Utilization_Ration < lowest_Credit_Utilization_Ration_Threshold):
        Suggestions_List.append('Your utilization ration is less than 30% 👍 , Please Maintain this ,to Create postive impact')
    
    elif( Credit_Utilization_Ration > lowest_Credit_Utilization_Ration_Threshold and
        Credit_Utilization_Ration < highest_Credit_Utilization_Ration_Threshold):
        Suggestions_List.append('Your Utilizing your credit card more than your usual ,It will create negitive impact , So use less than 30%')

    elif( Credit_Utilization_Ration > highest_Credit_Utilization_Ration_Threshold):
        Suggestions_List.append('Your Credit Utilization is too high, Try to Utilize less than 30%')

    if(len(Suggestions_List)==0):
        Suggestions_List.append('Youer Cibil Score was good 👍, Maintain like this')
        
    return Suggestions_List


st.title('Credit Score Classification Prediction Interface')

# Define loan types
loan_types = [
    "Credit-Builder Loan",
    "Personal Loan",
    "Debt Consolidation Loan",
    "Student Loan",
    "Payday Loan",
    "Mortgage Loan",
    "Auto Loan",
    "Home Equity Loan"
]

# Define occupations
occupations = [
    "Architect", "Developer", "Doctor", "Engineer", "Entrepreneur",
    "Journalist", "Lawyer", "Manager", "Mechanic", "Media Manager",
    "Musician", "Scientist", "Teacher", "Writer"
]

# Define payment behaviors
payment_behaviors = [
    "High-spent Medium-value payments",
    "High-spent Small-value payments",
    "Low-spent Large-value payments",
    "Low-spent Medium-value payments",
    "Low-spent Small-value payments"
]

# Define credit mix classifications
credit_mix_classifications = ["Bad", "Standard", "Good"]

Payment_of_min_classifications=["Yes","No"]

# Numeric inputs

inputs=[]

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=23, max_value=100) #0
    annual_income = st.number_input("Annual Income", value=500000) #1
    monthly_inhand_salary = annual_income/12    #2
    num_bank_accounts = st.number_input("Number of Bank Accounts", value=6) #3
    num_credit_card = st.number_input("Number of Credit Cards", value=4) #4
    interest_rate = st.number_input("Interest Rate", value=10.0) #5
    num_of_loan = st.number_input("Number of Loans", value=2) #6
    delay_from_due_date = st.number_input("Delay from Due Date", value=0) #7
    num_of_delayed_payment = st.number_input("Number of Delayed Payments", value=0) #8
    changed_credit_limit = st.number_input("Changed Credit Limit", value=10) #9
    num_credit_inquiries = st.number_input("Number of Credit Inquiries", value=2) #10

    credit_mix = st.selectbox("Credit Mix", credit_mix_classifications)
    credit_mix_mapping = { "Bad":0, "Standard":1, "Good":2 }
    credit_mix = credit_mix_mapping.get(credit_mix) #11

with col2:
    outstanding_debt = st.number_input("Outstanding Debt", value=23000) #12
    credit_utilization_ratio = st.slider("Credit Utilization Ratio", min_value=0, max_value=100, value=16) #13
    credit_history_years = st.text_input("Credit History", "4 years 7 months") 
    history = credit_history_years.split()
    # Calculate total credit history age in months
    total_credit_history_age = (int(history[0])* 12) + int(history[2]) #14

    total_emi_per_month = st.number_input("Total EMI per Month", value=24000) #15
    amount_invested_monthly = st.number_input("Amount Invested Monthly", value=1000) #16
    monthly_balance = st.number_input("Monthly Balance", value=12000) #17

    inputs = [age, annual_income, monthly_inhand_salary, num_bank_accounts, num_credit_card, interest_rate,
            num_of_loan, delay_from_due_date, num_of_delayed_payment, changed_credit_limit, num_credit_inquiries,
            credit_mix, outstanding_debt, credit_utilization_ratio, total_credit_history_age,
            total_emi_per_month, amount_invested_monthly, monthly_balance,0]

    # Checkboxes for loan types
    selected_loan_types = st.multiselect("Select Loan Types", loan_types) #18 - 25
    for loan in loan_types:
        if loan in selected_loan_types:
            inputs.append(1)
        else:
            inputs.append(0)


    selected_occupation = st.selectbox("Select Occupation", occupations) #26 - 39
    for occupation in occupations:
        if occupation in selected_occupation:
            inputs.append(1)
        else:
            inputs.append(0)


    pom = st.selectbox("Payment_of_Min Amount Yes", Payment_of_min_classifications)
    pom_mapping = { "Yes":1, "No":0 }
    pom = pom_mapping.get(pom) #40

    selected_payment_behavior = st.selectbox("Select Payment Behavior", payment_behaviors) #41 - 45
    for payment_behaviour in payment_behaviors:
        if payment_behaviour in selected_payment_behavior:
            inputs.append(1)
        else:
            inputs.append(0)

if st.button('Predict'):
    # Ensure the input data array is exactly 54 features long
    input_df = pd.DataFrame([inputs])

    # Scale the data
    scaled_data = scale_input(input_df, scaler)
    
    # Make prediction
    prediction = make_prediction(scaled_data, model)
    
    # Map the prediction to the corresponding Credit Mix category
    credit_score_mapping = {'Poor': 0,'Standard': 1, 'Good':2}
    for i in credit_score_mapping.keys():
        if credit_score_mapping[i] == prediction:
            credit_score = i
    st.write('Credit Score:', credit_score)
    
    suggestions = getSuggestions(inputs[1], inputs[3], inputs[4], inputs[5],
                                  inputs[6], inputs[7], inputs[8], inputs[13])
    # Display suggestions
    st.write('Suggestions:')
    for suggestion in suggestions:
        st.write('-', suggestion)
