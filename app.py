import streamlit as st

# Main function for the app
def main():
    st.title("MSME Loan Proposal Application")

    # Navigation
    pages = ["Home", "Loan Application", "Status Check"]
    selected_page = st.sidebar.selectbox("Select Page", pages)
    
    if selected_page == "Home":
        display_home()
    elif selected_page == "Loan Application":
        display_loan_application()
    elif selected_page == "Status Check":
        display_status_check()

# Function to display the home page
def display_home():
    st.header("Welcome to the MSME Loan Proposal Application")
    st.write("Navigate through the application using the sidebar.")

# Function to handle loan application form
def display_loan_application():
    st.header("Loan Application Form")
    
    with st.form(key='loan_form'):
        applicant_name = st.text_input("Applicant Name")
        loan_amount = st.number_input("Loan Amount", min_value=1000, max_value=1000000, step=1000)
        loan_type = st.selectbox("Select Loan Type", ["Startup", "Expansion", "Refinancing"])
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            st.session_state.applicant_name = applicant_name
            st.session_state.loan_amount = loan_amount
            st.session_state.loan_type = loan_type
            st.success("Loan application submitted!")

# Function to check loan application status
def display_status_check():
    st.header("Check Loan Application Status")
    
    if 'applicant_name' in st.session_state:
        st.write(f"Applicant Name: {st.session_state.applicant_name}")
        st.write(f"Loan Amount: {st.session_state.loan_amount}")
        st.write(f"Loan Type: {st.session_state.loan_type}")
    else:
        st.warning("No application submitted yet.")

if __name__ == "__main__":
    main()