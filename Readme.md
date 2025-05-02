#### Personal Wealth Manager 💰

A simple, browser-based financial tracking app built with Python, Flask, Pandas and Streamlit. Track your expenses, manage your investment portfolio, and calculate your savings effortlessly.

## 🚀 Overview
This project helps you manage your personal finances by:

# Tracking monthly expenses.
Managing a share portfolio with real-time profit calculations.
Calculating savings based on salary, expenses, and portfolio spends.

The app features an attractive welcome animation, intuitive navigation, and data persistence using CSV files.

## 🛠️ Setup Instructions
Follow these steps to run the app locally:

# Clone the repository:
git clone https://github.com/thecoderji/personal_wealth_manager.git
cd personal_wealth_manager


# Set up a virtual environment:
python -m venv .venv
.venv\Scripts\activate  # On macOS/Linux: source .venv/bin/activate


# Install dependencies
Install the required packages one by one:
pip install streamlit
pip install pandas
pip install flask


# Run the app:
streamlit run app.py


# Open in browser:

Visit http://localhost:8501 to see the app in action.




## ✨ Features
# 1. Welcome Page

A visually appealing welcome animation with a typing effect and progress bar.
Screenshot: ![Screenshot 2025-05-02 224649](https://github.com/user-attachments/assets/913d7d9d-f1a6-4c23-8d84-6f0cd888e5c4)


# 2. Home Page

Navigate to Expense Tracker or Portfolio Viewer with a clean, two-button layout.
Screenshot: ![Screenshot 2025-05-02 224714](https://github.com/user-attachments/assets/93a3604c-e099-4c60-bf67-157649623561)


# 3. Expense Tracker

Update your monthly salary.
Add expenses (Name, Amount) and view them in a table.
See portfolio spend and current savings for the month.
Screenshot: ![Screenshot 2025-05-02 224951](https://github.com/user-attachments/assets/13ed05f0-ae2e-4994-889a-cb8104fc241c)


# 4. Portfolio Viewer

View shares in a row-wise layout for better space utilization.
Add new shares (Share Name, Quantity, Buy Price, Total Amount).
See portfolio spend and current savings.
Screenshot: ![Screenshot 2025-05-02 224859](https://github.com/user-attachments/assets/45e5a257-7c27-48d9-9ffe-f470a2529dab)


# 5. Share Details

View detailed info about a share (Name, Quantity, Buy Price, Buy Date, Current Price, Profit).
Update the current price of a share.
Navigate back to Portfolio Viewer or Home.
Screenshot: ![Screenshot 2025-05-02 224922](https://github.com/user-attachments/assets/04570836-6992-47ca-8f34-81cd1ce1ef07)



## 📂 Project Structure
personal_wealth_manager/
│
├── app.py   =>   Main Streamlit app
├── data/   =>   Folder for CSV data files (not tracked in Git)
│   ├── expenses.csv    =>   Stores expense data (ignored by .gitignore)
│   ├── portfolio.csv   =>   Stores portfolio data (ignored by .gitignore)
│   ├── salary.csv    =>   Stores monthly salary data (ignored by .gitignore)
├── .gitignore    =>   Ignored files (e.g., .venv, CSV files)
└── README.md    =>   Project documentation


## 📋 Requirements

Python: 3.12.3 or higher
Dependencies: Streamlit, Pandas, Flask
Virtual Environment: Recommended for dependency isolation


## 📜 License
This project is open-source and available under the MIT License.

## 🙌 Acknowledgments

Built with ❤️ using Streamlit and Pandas.
Thanks to the open-source community for amazing tools and libraries!

