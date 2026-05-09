# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="MSME Loan Proposal System", layout="wide")

# -----------------------------
# Helper Functions
# -----------------------------
def get_msme_category(turnover):
    if turnover <= 500:
        return "Micro"
    elif turnover <= 5000:
        return "Small"
    return "Medium"

def assess_cibil(score):
    if score >= 750:
        return "Excellent", "Low Risk", 30
    elif score >= 700:
        return "Very Good", "Good Risk", 25
    elif score >= 650:
        return "Good", "Moderate Risk", 20
    elif score >= 600:
        return "Fair", "Higher Risk", 10
    return "Poor", "High Risk", 0

def calculate_ratios(revenue, expenses, profit, assets, liabilities, current_assets, current_liabilities):
    profit_margin = (profit / revenue * 100) if revenue else 0
    current_ratio = (current_assets / current_liabilities) if current_liabilities else 0
    debt_equity = (liabilities / (assets - liabilities)) if (assets - liabilities) > 0 else 0
    roa = (profit / assets * 100) if assets else 0
    return profit_margin, current_ratio, debt_equity, roa

def calculate_score(cibil, profit_margin, current_ratio, debt_equity, loan_amount, turnover):
    score = 0

    _, _, cibil_points = assess_cibil(cibil)
    score += cibil_points

    if profit_margin >= 15:
        score += 20
    elif profit_margin >= 10:
        score += 15
    elif profit_margin >= 5:
        score += 10

    if current_ratio >= 1.5:
        score += 15
    elif current_ratio >= 1:
        score += 10

    if debt_equity <= 1:
        score += 15
    elif debt_equity <= 1.5:
        score += 10

    if loan_amount <= turnover * 0.25:
        score += 20
    elif loan_amount <= turnover * 0.50:
        score += 10

    return score

def get_result(score):
    if score >= 80:
        return "✅ APPROVED", "Excellent profile. Strong approval recommendation."
    elif score >= 60:
        return "🟡 CONDITIONAL APPROVAL", "Can be approved with conditions/collateral."
    elif score >= 45:
        return "🟠 NEEDS REVIEW", "Further verification required."
    return "❌ REJECTED", "Risk profile is high."

# -----------------------------
# UI
# -----------------------------
st.title("🏦 MSME Loan Proposal System")
st.markdown("### Professional Loan Assessment App for Indian Banks")

tabs = st.tabs(["Business Info", "Financials", "Loan Request", "Final Report"])

# -----------------------------
# TAB 1
# -----------------------------
with tabs[0]:
    st.subheader("Business Information")

    col1, col2 = st.columns(2)

    with col1:
        business_name = st.text_input("Business Name")
        owner_name = st.text_input("Owner Name")
        business_type = st.selectbox("Business Type", ["Manufacturing", "Trading", "Services"])
        reg_type = st.selectbox("Registration Type", ["Proprietorship", "Partnership", "Pvt Ltd", "LLP"])

    with col2:
        turnover = st.number_input("Annual Turnover (₹ Lakhs)", min_value=0.0, value=100.0)
        cibil = st.slider("CIBIL Score", 300, 900, 750)
        years = st.number_input("Years in Business", min_value=0, value=3)

    category = get_msme_category(turnover)
    st.success(f"MSME Category: {category}")

# -----------------------------
# TAB 2
# -----------------------------
with tabs[1]:
    st.subheader("Financial Details")

    col1, col2 = st.columns(2)

    with col1:
        revenue = st.number_input("Gross Revenue (₹ Lakhs)", min_value=0.0, value=100.0)
        expenses = st.number_input("Operating Expenses (₹ Lakhs)", min_value=0.0, value=70.0)
        profit = st.number_input("Net Profit (₹ Lakhs)", min_value=0.0, value=20.0)

    with col2:
        assets = st.number_input("Total Assets (₹ Lakhs)", min_value=0.0, value=150.0)
        liabilities = st.number_input("Total Liabilities (₹ Lakhs)", min_value=0.0, value=60.0)
        current_assets = st.number_input("Current Assets (₹ Lakhs)", min_value=0.0, value=80.0)
        current_liabilities = st.number_input("Current Liabilities (₹ Lakhs)", min_value=0.0, value=40.0)

    pm, cr, de, roa = calculate_ratios(
        revenue, expenses, profit, assets, liabilities, current_assets, current_liabilities
    )

    st.write("### Financial Ratios")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Profit Margin", f"{pm:.2f}%")
    r2.metric("Current Ratio", f"{cr:.2f}")
    r3.metric("Debt/Equity", f"{de:.2f}")
    r4.metric("ROA", f"{roa:.2f}%")

# -----------------------------
# TAB 3
# -----------------------------
with tabs[2]:
    st.subheader("Loan Requirement")

    col1, col2 = st.columns(2)

    with col1:
        wc_loan = st.number_input("Working Capital Loan (₹ Lakhs)", min_value=0.0, value=20.0)
        term_loan = st.number_input("Term Loan (₹ Lakhs)", min_value=0.0, value=30.0)

    with col2:
        tenure = st.number_input("Tenure (Years)", min_value=1, value=5)
        interest = st.number_input("Interest Rate %", min_value=1.0, value=11.0)

    total_loan = wc_loan + term_loan
    st.info(f"Total Loan Required: ₹ {total_loan:.2f} Lakhs")

# -----------------------------
# TAB 4
# -----------------------------
with tabs[3]:
    st.subheader("Loan Decision Report")

    score = calculate_score(cibil, pm, cr, de, total_loan, turnover)
    decision, remarks = get_result(score)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Overall Score", score)
        st.success(decision)

    with col2:
        st.write("### Remarks")
        st.info(remarks)

    st.write("---")

    report = {
        "Business Name": business_name,
        "Owner Name": owner_name,
        "Business Type": business_type,
        "Registration": reg_type,
        "Turnover": turnover,
        "CIBIL": cibil,
        "MSME Category": category,
        "Total Loan": total_loan,
        "Profit Margin": round(pm, 2),
        "Current Ratio": round(cr, 2),
        "Debt Equity": round(de, 2),
        "ROA": round(roa, 2),
        "Final Score": score,
        "Decision": decision
    }

    df = pd.DataFrame(report.items(), columns=["Field", "Value"])
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download Report CSV",
        csv,
        file_name="msme_loan_report.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("Powered by Streamlit | MSME Loan Proposal Professional Edition")