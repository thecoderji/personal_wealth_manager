import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

# File paths
EXPENSES_FILE = "data/expenses.csv"
PORTFOLIO_FILE = "data/portfolio.csv"
SALARY_FILE = "data/salary.csv"

# Initialize CSV files
def init_files():
    if not os.path.exists("data"):
        os.makedirs("data")

    # Initialize expenses.csv
    if not os.path.exists(EXPENSES_FILE) or os.path.getsize(EXPENSES_FILE) == 0:
        pd.DataFrame(columns=["Date", "Name", "Amount"]).to_csv(EXPENSES_FILE, index=False)

    # Initialize portfolio.csv
    if not os.path.exists(PORTFOLIO_FILE) or os.path.getsize(PORTFOLIO_FILE) == 0:
        pd.DataFrame(columns=["Share_Name", "Quantity", "Buy_Price", "Buy_Date", "Last_Update_Date", "Current_Price"]).to_csv(PORTFOLIO_FILE, index=False)

    # Initialize salary.csv
    if not os.path.exists(SALARY_FILE) or os.path.getsize(SALARY_FILE) == 0:
        pd.DataFrame([[datetime.now().strftime("%Y-%m"), 0]], columns=["Month", "Salary"]).to_csv(SALARY_FILE, index=False)

init_files()

# Helper functions
def get_salary():
    try:
        df = pd.read_csv(SALARY_FILE)
        current_month = datetime.now().strftime("%Y-%m")
        row = df[df["Month"] == current_month]
        return float(row["Salary"].iloc[0]) if not row.empty else 0
    except (pd.errors.EmptyDataError, FileNotFoundError):
        # If file is empty or not found, reinitialize it and return 0
        pd.DataFrame([[datetime.now().strftime("%Y-%m"), 0]], columns=["Month", "Salary"]).to_csv(SALARY_FILE, index=False)
        return 0

def update_salary(salary):
    df = pd.DataFrame([[datetime.now().strftime("%Y-%m"), salary]], columns=["Month", "Salary"])
    df.to_csv(SALARY_FILE, index=False)

def get_expenses():
    try:
        return pd.read_csv(EXPENSES_FILE)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        # If file is empty or not found, reinitialize it and return empty DataFrame
        pd.DataFrame(columns=["Date", "Name", "Amount"]).to_csv(EXPENSES_FILE, index=False)
        return pd.DataFrame(columns=["Date", "Name", "Amount"])

def get_portfolio():
    try:
        return pd.read_csv(PORTFOLIO_FILE)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        # If file is empty or not found, reinitialize it and return empty DataFrame
        pd.DataFrame(columns=["Share_Name", "Quantity", "Buy_Price", "Buy_Date", "Last_Update_Date", "Current_Price"]).to_csv(PORTFOLIO_FILE, index=False)
        return pd.DataFrame(columns=["Share_Name", "Quantity", "Buy_Price", "Buy_Date", "Last_Update_Date", "Current_Price"])

def get_monthly_portfolio_spend():
    df = get_portfolio()
    current_month = datetime.now().strftime("%Y-%m")
    monthly = df[df["Buy_Date"].str.startswith(current_month)]
    return sum(monthly["Quantity"] * monthly["Buy_Price"]) if not monthly.empty else 0

def get_savings():
    salary = get_salary()
    expenses = get_expenses()["Amount"].sum()
    portfolio_spend = get_monthly_portfolio_spend()
    return salary - expenses - portfolio_spend

# Welcome page with enhanced animation
def welcome_page():
    welcome_text = "Welcome to Personal Wealth Manager"

    # Typing effect for the welcome message
    placeholder = st.empty()
    for i in range(len(welcome_text) + 1):
        placeholder.markdown(f"<h1 style='text-align: center;'>{welcome_text[:i]}</h1>", unsafe_allow_html=True)
        time.sleep(0.05)  # Speed of typing effect

    # Progress bar animation
    progress_text = st.empty()
    progress_bar = st.progress(0)
    for i in range(101):
        progress_text.markdown(f"**Loading... {i}%**")
        progress_bar.progress(i)
        time.sleep(0.03)  # Speed of progress bar

    # Clear the progress bar and text
    progress_text.empty()
    progress_bar.empty()

    # Redirect to home page
    st.session_state.page = "home"
    st.rerun()

# Main app
def main():
    # Session state for page navigation
    if "page" not in st.session_state:
        st.session_state.page = "welcome"

    # Page routing
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "home":
        st.markdown("# Personal Wealth Manager")
        st.markdown("### Home")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Expense Tracker"):
                st.session_state.page = "expense_tracker"
                st.rerun()
        with col2:
            if st.button("Portfolio Viewer"):
                st.session_state.page = "portfolio_viewer"
                st.rerun()
    elif st.session_state.page == "expense_tracker":
        st.markdown("### Expense Tracker")
        if st.button("🏠 Back to Home"):
            st.session_state.page = "home"
            st.rerun()

        # Salary display and update
        salary = get_salary()
        st.markdown(f"**Monthly Salary: ₹{salary}**")
        new_salary = st.number_input("Update Monthly Salary", min_value=0.0, step=1000.0, value=salary)
        if st.button("Update Salary"):
            update_salary(new_salary)
            st.success("Salary updated!")
            st.rerun()

        # Expenses table
        expenses = get_expenses()
        if not expenses.empty:
            st.markdown("**Expenses**")
            st.table(expenses[["Name", "Amount"]])

        # Add expense form
        st.markdown("**Add Expense**")
        with st.form("expense_form"):
            name = st.text_input("Expense Name")
            amount = st.number_input("Amount", min_value=0.0, step=100.0)
            submit = st.form_submit_button("Add")
            if submit and name and amount:
                new_expense = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), name, amount]], 
                                        columns=["Date", "Name", "Amount"])
                expenses = pd.concat([expenses, new_expense], ignore_index=True)
                expenses.to_csv(EXPENSES_FILE, index=False)
                st.success("Expense added!")
                st.rerun()

        # Summary
        portfolio_spend = get_monthly_portfolio_spend()
        savings = get_savings()
        st.markdown(f"**Portfolio Spend This Month: ₹{portfolio_spend}**")
        st.markdown(f"**Current Savings: ₹{savings}**")

    elif st.session_state.page == "portfolio_viewer":
        st.markdown("### Portfolio Viewer")
        if st.button("🏠 Back to Home"):
            st.session_state.page = "home"
            st.rerun()

        # Portfolio list (row-wise)
        portfolio = get_portfolio()
        if not portfolio.empty:
            st.markdown("**Shares**")
            cols = st.columns(5)  # 5 shares per row
            for idx, row in portfolio.iterrows():
                col = cols[idx % 5]  # Cycle through columns
                with col:
                    if st.button(row["Share_Name"]):
                        st.session_state.share_name = row["Share_Name"]
                        st.session_state.page = "share_details"
                        st.rerun()

        # Add new share form
        st.markdown("**Add New Share**")
        with st.form("share_form"):
            share_name = st.text_input("Share Name")
            quantity = st.number_input("Quantity", min_value=1, step=1)
            buy_price = st.number_input("Buy Price per Share", min_value=0.0, step=10.0)
            total_amount = st.number_input("Total Amount", min_value=0.0, step=10.0)
            submit = st.form_submit_button("Add")
            if submit and share_name and quantity and buy_price and total_amount:
                if abs(total_amount - quantity * buy_price) > 0.01:  # Small tolerance for float errors
                    st.error("Total Amount does not match Quantity * Buy Price!")
                else:
                    new_share = pd.DataFrame([[share_name, quantity, buy_price, 
                                            datetime.now().strftime("%Y-%m-%d"),
                                            datetime.now().strftime("%Y-%m-%d"), buy_price]],
                                        columns=["Share_Name", "Quantity", "Buy_Price", "Buy_Date", 
                                                    "Last_Update_Date", "Current_Price"])
                    portfolio = pd.concat([portfolio, new_share], ignore_index=True)
                    portfolio.to_csv(PORTFOLIO_FILE, index=False)
                    st.success("Share added!")
                    st.rerun()

        # Summary
        portfolio_spend = get_monthly_portfolio_spend()
        savings = get_savings()
        st.markdown(f"**Portfolio Spend This Month: ₹{portfolio_spend}**")
        st.markdown(f"**Current Savings: ₹{savings}**")

    elif st.session_state.page == "share_details":
        st.markdown("### Share Details")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🏠 Back to Home"):
                st.session_state.page = "home"
                st.rerun()
        with col2:
            if st.button("🔙 Back to Portfolio"):
                st.session_state.page = "portfolio_viewer"
                st.rerun()

        share_name = st.session_state.get("share_name", "")
        portfolio = get_portfolio()
        share = portfolio[portfolio["Share_Name"] == share_name]
        if share.empty:
            st.error("Share not found!")
            return

        share = share.iloc[0]
        profit = (share["Current_Price"] - share["Buy_Price"]) * share["Quantity"]
        details = pd.DataFrame({
            "Field": ["Share Name", "Quantity", "Buy Price", "Buy Date", 
                    "Last Update Date", "Current Price", "Profit Till Today"],
            "Value": [share["Share_Name"], share["Quantity"], f"₹{share['Buy_Price']}",
                    share["Buy_Date"], share["Last_Update_Date"], f"₹{share['Current_Price']}",
                    f"₹{profit}"]
        })
        st.table(details)

        # Update current price
        st.markdown("**Update Current Price**")
        with st.form("price_form"):
            current_price = st.number_input("Current Price", min_value=0.0, step=10.0, value=float(share["Current_Price"]))
            submit = st.form_submit_button("Update")
            if submit:
                portfolio.loc[portfolio["Share_Name"] == share_name, "Current_Price"] = current_price
                portfolio.loc[portfolio["Share_Name"] == share_name, "Last_Update_Date"] = datetime.now().strftime("%Y-%m-%d")
                portfolio.to_csv(PORTFOLIO_FILE, index=False)
                st.success("Price updated!")
                st.rerun()

if __name__ == "__main__":
    st.set_page_config(page_title="Personal Wealth Manager", page_icon="💰")
    main()