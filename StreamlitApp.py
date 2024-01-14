# Import necessary libraries
import streamlit as st
import openai
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import math
import numpy as np
import plotly.graph_objects as go

# Set OpenAI API key
openai.api_key = "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"


# Function to get the OpenAI response
class OpenAIAPI:
    @staticmethod
    def get_response(prompt, history):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=history,
                max_tokens=150,
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            st.error(f"There was an issue processing your request. Please try again.")
            st.error(f"Error details: {str(e)}")

# Function for selecting expense category
def select_expense_category():
    st.write("Please select an expense category:")
    expense_categories = ["Groceries", "Utilities", "Entertainment", "financial_advice", "create_note", "manage_bills", "Others"]
    expense_category = st.selectbox("Expense Category", expense_categories)
    return expense_category.lower()  # Um sicherzustellen, dass die Eingabe klein geschrieben ist

# Function for the chat page
def chat_page(history):
    st.subheader("Chat with FinanceBuddy")

     # User selection for the category
    selected_category = select_expense_category()

     # Unique key for the button
    send_button_key = "send_button"

    # Lists to store user questions and assistant responses
    user_questions = []
    assistant_responses = []

     # Loop for user interaction
    num_questions = 3
    for question_number in range(num_questions):
         # User input with a unique key
        user_input = st.text_input(f"Enter question {question_number + 1}:")

        
    # Button for sending user query with a unique key
        if st.button("Send", key=f"{send_button_key}_{question_number}"):
            if user_input:
                # Improved context usage
                user_message = user_input

                # Add the selected category to the user query
                user_message = f"{user_message} (Category: {selected_category})"
                history.append({"role": "user", "content": user_message})

                # Save user question in the list
                user_questions.append(user_message)

                # Check if the user query corresponds to any of the new categories
                if "create a note:" in user_message.lower():
                    create_note(history)
                elif "add a bill:" in user_message.lower():
                    manage_bills(history)
                elif "request financial advice:" in user_message.lower():
                    financial_advice(history)
                else:
                     # Default behavior for unrecognized categories
                    bot_response = OpenAIAPI.get_response(user_message, history)
                    history.append({"role": "assistant", "content": bot_response})
                    assistant_responses.append(bot_response)

    # Display the entire chat history at the end of the loop
    st.subheader("Chat History")
    for entry in history:
        if entry["role"] == "user":
            st.text(f"You: {entry['content']}")
        elif entry["role"] == "assistant":
            st.text(f"FinanceBuddy: {entry['content']}")
        elif entry["role"] == "system":
            st.text(f"System: {entry['content']}")

    # Display collected user questions and assistant responses at the end of the loop
    st.subheader("User Questions and Assistant Responses")
    for i, (question, response) in enumerate(zip(user_questions, assistant_responses), 1):
        st.text(f"Question {i}: {question}")
        st.text(f"Assistant Response {i}: {response}")
    # Function for the "create a note" category
def create_note(history):
    user_input = st.text_input("Enter your note:")
    if st.button("Save Note"):
        if user_input:
            history.append({"role": "user", "content": f"Create a note: {user_input}"})
            bot_response = OpenAIAPI.get_response(user_input, history)
            history.append({"role": "assistant", "content": bot_response})
            st.write("FinanceBuddy:", bot_response)
        else:
            st.warning("Please enter a note.")
       
        # Function for the "add a bill" category
def manage_bills(history):
    user_input = st.text_input("Enter your bill details:")
    if st.button("Add Bill"):
        if user_input:
            history.append({"role": "user", "content": f"Add a bill: {user_input}"})
            bot_response = OpenAIAPI.get_response(user_input, history)
            history.append({"role": "assistant", "content": bot_response})
            st.write("FinanceBuddy:", bot_response)
        else:
            st.warning("Please enter bill details.")

# Function for the "request financial advice" category
def financial_advice(history):
    user_input = st.text_input("Ask for financial advice:")
    if st.button("Get Advice"):
        if user_input:
            history.append({"role": "user", "content": f"Request financial advice: {user_input}"})
            bot_response = OpenAIAPI.get_response(user_input, history)
            history.append({"role": "assistant", "content": bot_response})
            st.write("FinanceBuddy:", bot_response)
        else:
             st.warning("Please ask for financial advice.")

# Main function to run the Streamlit app
def main():
    # Set Streamlit theme
    st.set_page_config(page_title="FinanceBuddy", page_icon="💰", layout="wide")

    # Initialize chat history
    history = [{"role": "system", "content": "Your FinanceBuddy, your personal finance assistant."}]

    # Sidebar navigation
    menu = ["Home", "Chat", "Budget", "Investments", "Loan Calculator", "Contact"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Home page
    if choice == "Home":
        home_page()

    # Chat page
    elif choice == "Chat":
        chat_page(history)

    # Budget page
    elif choice == "Budget":
        budget_page(history)

    # Investments page
    elif choice == "Investments":
        investments_page(history)

    # Loan Calculator page
    elif choice == "Loan Calculator":
        loan_calculator_page()

    # Contact page
    elif choice == "Contact":
        contact_page()

# Home page content
def home_page():
    st.subheader("Welcome to FinanceBuddy!")
    st.write("Your personal finance assistant is here to help you.")

    # Add welcome text
    st.write(
        "Manage your finances, get investment advice, create notes, and more with FinanceBuddy. "
        "Use the sidebar to navigate to different sections and explore the features."
    )

    # Add a brief guide
    st.subheader("Getting Started:")
    st.write(
        "1. **Chat:** Interact with FinanceBuddy through the Chat page. Ask questions, get financial advice, and more."
        "\n2. **Budget:** Manage your budget by entering your monthly income, expenses, and savings goals."
        "\n3. **Investments:** Simulate and analyze your investments with the Investment page."
        "\n4. **Loan Calculator:** Calculate your loan payments and get recommendations."
        "\n5. **Contact Us:** Have questions or suggestions? Visit the Contact page."
    )

    # Add a brief summary of features
    st.subheader("Key Features:")
    st.write(
        "1. **Chat with FinanceBuddy:** Ask questions and receive personalized financial advice."
        "\n2. **Budget Management:** Track your monthly income, expenses, and savings goals."
        "\n3. **Investment Simulation:** Estimate future values and analyze risks for your investments."
        "\n4. **Loan Calculator:** Calculate loan payments and get recommendations."
    )

    # Add recommendations for using the site
    st.subheader("Page Recommendations:")
    st.write(
        "1. **Explore:** Navigate through different sections using the sidebar to explore FinanceBuddy's features."
        "\n2. **Learn:** Visit the Chat page to learn more about financial management and get personalized advice."
        "\n3. **Plan:** Use the Budget page to plan your monthly finances and set savings goals."
        "\n4. **Simulate:** Analyze potential returns and risks with the Investments page."
        "\n5. **Calculate:** Estimate loan payments and receive recommendations with the Loan Calculator page."
    )

# Function to calculate the number of months needed to reach a savings goal
def calculate_months_to_goal(savings, savings_goal):
    if savings <= 0:
        return math.inf  # Return infinity if savings are not positive
    else:
        return math.ceil(savings_goal / savings)
# Function to calculate the budget per person
def calculate_budget_per_person(monthly_expenses, num_people):
    return monthly_expenses / num_people if num_people > 0 else 0
# Budget page content
def budget_page(history):
    st.subheader("Budget Management")
    
    #Input fields
    monthly_income = st.number_input("Monthly Income:", help="Enter your total monthly income.")
    monthly_expenses = st.number_input("Monthly Expenses:", help="Enter your total monthly expenses.")
    num_people = st.number_input("Number of People:", help="Enter the number of people your budget will cover.")
    savings_goal = st.number_input("Savings Goal:", help="Set a savings goal for the future.")

    # Check if all relevant inputs are zero
    if all(value == 0 for value in [monthly_income, monthly_expenses, num_people]):
        st.warning("Please enter non-zero values for Monthly Income, Monthly Expenses, and Number of People.")
        return

    # Check if num_people is greater than 0
    if num_people <= 0:
        st.warning("Number of People must be greater than 0.")
        return

    # Calculations
    savings = monthly_income - monthly_expenses
    monthly_expenses_per_person = calculate_budget_per_person(monthly_expenses, num_people)
    savings_per_person = monthly_income / num_people - monthly_expenses_per_person
    
    st.write(f"Your available savings amount is: {savings:.2f} EUR")
    st.write(f"Monthly Expenses per person: {monthly_expenses_per_person:.2f} EUR")
    st.write(f"Savings per person: {savings_per_person:.2f} EUR")

    # Expense categories
    expense_categories = st.multiselect("Add Expense Categories:", ["Groceries", "Utilities", "Entertainment", "Others"], 
                                       help="Select the categories that represent your monthly expenses.")

    if expense_categories:
        # Table for detailed analysis
        st.subheader("Detailed Expense Analysis:")
        expense_data = {'Expense Category': expense_categories, 'Amount Spent': []}
        for category in expense_categories:
            amount_spent = st.number_input(f"Amount Spent on {category}:", key=category)
            expense_data['Amount Spent'].append(amount_spent)

        expense_df = pd.DataFrame(expense_data)

        # Pie chart for expense categories
        fig_pie = go.Figure(go.Pie(labels=expense_df['Expense Category'], values=expense_df['Amount Spent'], hole=0.4))
        fig_pie.update_layout(title="Expense Breakdown")
        st.plotly_chart(fig_pie)

        # Average amount for all categories
        avg_amount_spent = expense_df['Amount Spent'].mean()

        # Budget suggestion per category
        st.subheader("Budget Suggestions per Category:")
        for category in expense_categories:
            suggested_budget = calculate_budget_per_person(avg_amount_spent, num_people)
            st.write(f"Suggested Budget for {category}: {suggested_budget:.2f} EUR per person")

            # Analysis and recommendations for each category
            st.subheader(f"Analysis for {category}:")
            st.write(f"You spent {amount_spent:.2f} EUR on {category}.")
            
            # Interpretation
            if amount_spent > suggested_budget:
                st.write(f"You spent more than the suggested budget for {category}. Consider reviewing your expenses in this category.")
            elif amount_spent < suggested_budget:
                st.write(f"You spent less than the suggested budget for {category}. Good job! Consider saving the difference.")

            # Savings recommendations
            st.subheader(f"Savings Recommendations for {category}:")
            st.write(
                f"1. **Review Expenses:** Analyze your spending patterns in {category}. Look for areas where you can cut costs.\n"
                f"2. **Set Limits:** Consider setting a monthly limit for {category} to control your spending.\n"
                f"3. **Explore Alternatives:** Look for more cost-effective alternatives without compromising quality.\n"
            )

    # Visualization of total expenses
    labels = ["Earnings", "Expenses", "Savings"]  # Umbenannt, um klarere Bezeichnungen zu verwenden
    values = [monthly_income, -monthly_expenses, savings]
    colors = ["green", "red", "blue"]

     # Enhance chart: Percentage, tips, history, budget overrun
    fig = go.Figure()

    # Percentage of expenses compared to income
    fig.add_trace(go.Bar(x=labels, y=[val/monthly_income * 100 for val in values], text=[f"{val:.2f}%" for val in values], textposition='inside', 
                         marker=dict(color=colors)))

    # Add savings per person
    fig.add_trace(go.Bar(x=["Savings per person"], y=[savings_per_person], text=[f"{savings_per_person:.2f} EUR"], textposition='outside', marker=dict(color="blue")))

    # Line chart for savings history
    savings_history = [monthly_income - monthly_expenses]  # Hier können Sie Ihre tatsächlichen Ersparnisse im Laufe der Zeit hinzufügen
    fig.add_trace(go.Scatter(x=[f"Month {i}" for i in range(1, len(savings_history) + 1)], y=savings_history, mode='lines+markers', name='Savings History'))

   # Display budget overrun (if applicable)
    if savings < 0:
        fig.add_shape(go.layout.Shape(type="line", x0=-0.5, x1=2.5, y0=0, y1=0, line=dict(color="black", width=2)))

    fig.update_layout(title="Budget Breakdown and Analysis", barmode='stack', showlegend=False)

  # Display chart
    st.plotly_chart(fig)

    # Interpretation Text
    st.subheader("Budget Interpretation:")
    st.write(
        f"The budget breakdown visualizes your monthly financial situation. "
        f"You have an income of {monthly_income:.2f} EUR and monthly expenses of {-monthly_expenses:.2f} EUR, "
        f"resulting in savings of {savings:.2f} EUR."
    )

    # Calculate time to savings goal
    if savings_goal > 0:
        months_to_goal = calculate_months_to_goal(savings, savings_goal)
        st.write(f"You will reach your savings goal in {months_to_goal} months.")

    #Overall budget suggestion for all categories together
    if expense_categories:
        st.subheader("Overall Budget Suggestions:")
        suggested_budget_all = calculate_budget_per_person(avg_amount_spent * len(expense_categories), num_people)
        st.write(f"Suggested Overall Budget for all Categories: {suggested_budget_all:.2f} EUR per person")

    # Additional Budget Insights
    st.subheader("Additional Budget Insights:")
    st.write(
        "Consider reviewing your monthly expenses to identify areas where you can save. \n"
        "Creating a detailed budget plan can help you manage your finances more effectively."
    )

    # Recommendations
    st.subheader("Budget Recommendations:")
    st.write(
        "1. **Emergency Fund:** Ensure you have an emergency fund to cover unexpected expenses.\n"
        "2. **Expense Review:** Regularly review your expenses and cut unnecessary costs.\n"
        "3. **Budget Plan:** Create a detailed budget plan to track your income and expenses.\n"
    )
# Function to calculate the volatility of returns
def calculate_volatility(returns):
    # Function to calculate the volatility of returns
    return np.std(returns)
# Function to calculate the Sharpe ratio
def calculate_sharpe_ratio(returns):
    # Function to calculate the Sharpe ratio
    average_return = np.mean(returns)
    volatility = calculate_volatility(returns)
    risk_free_rate = 0.01  # You can adjust this based on your assumption for the risk-free interest rate
    
    # Modified calculation of Sharpe ratio
    excess_return = average_return - risk_free_rate
    sharpe_ratio = excess_return / volatility if volatility != 0 else 0
    
    return sharpe_ratio

# Investments page content
def investments_page(history):
    st.subheader("Investments")
    
    # User inputs for the investment
    investment_amount = st.number_input("Investment Amount:")
    investment_return = st.slider("Expected Return (%)", 0, 100, 5)
    investment_period = st.slider("Investment Period (Years)", 1, 30, 10)
    
    # Check if all relevant inputs are zero
    if all(value == 0 for value in [investment_amount, investment_return, investment_period]):
        st.warning("Please enter non-zero values for Investment Amount, Expected Return, and Investment Period.")
        return
    
    # Generate simulated returns (for demonstration purposes)
    returns = np.random.normal(loc=investment_return / 100, scale=0.2, size=investment_period * 252)
    
    total_return = investment_amount * (1 + investment_return / 100) ** investment_period
    compound_interest = total_return - investment_amount
    
    # Display the calculated values
    st.write(f"Your estimated future value is: {total_return:.2f} USD")
    st.write(f"Compound Interest earned: {compound_interest:.2f} USD")
    
    # User's investment goal
    investment_goal = st.number_input("Investment Goal:", min_value=0.0, step=100.0, help="Set a financial goal for your investment.")
    
    if investment_goal > 0:
        percentage_to_goal = (total_return / investment_goal) * 100
        st.write(f"You have reached {percentage_to_goal:.2f}% of your investment goal.")
    
    # Visualization of the investment breakdown using Plotly Express
    labels_investment = ["Invested Capital", "Compound Interest"]
    values_investment = [investment_amount, compound_interest]
    colors_investment = ["orange", "lightblue"]
    
    fig_investment = px.pie(
        names=labels_investment,
        values=values_investment,
        title='Investment Breakdown',
        color=labels_investment,
        color_discrete_map=dict(zip(labels_investment, colors_investment)),
        hole=0.4,
        labels={'label': 'Investment Breakdown', 'value': 'Amount (USD)'}
    )
    fig_investment.update_traces(textinfo="percent+label", pull=[0, 0.1])
    st.plotly_chart(fig_investment)

     # Interpretation of the investment breakdown
    st.subheader("Investment Breakdown Interpretation:")
    st.write(
        "The investment breakdown visualizes the distribution of your investment. Here's an interpretation of the components:"
    )
    st.write(
        f"Invested Capital: The initial amount you invested is {investment_amount:.2f} USD."
    )
    st.write(
        f"Compound Interest: The additional amount earned through compounded returns is {compound_interest:.2f} USD."
    )
    st.write(
        "Understanding this breakdown helps you recognize the impact of compounding on your investment over time."
    )

    
    # Risk analysis
    volatility = calculate_volatility(returns)
    sharpe_ratio = calculate_sharpe_ratio(returns)
    
    st.subheader("Risk Analysis:")
    st.write(f"Volatility (Risk): {volatility:.2%}")
    st.write(f"Sharpe Ratio: {sharpe_ratio:.4f}")
    # Interpretation of the risk analysis
    st.subheader("Risk Analysis Interpretation:")
    st.write(
            "The risk analysis provides insights into the stability and attractiveness of your investment. Here is an interpretation of the results:"
        )
    st.write(
            f"Volatility (Risk): Higher volatility of {volatility:.2%} indicates greater fluctuations, which may imply higher risk."
        )
    st.write(
            f"Sharpe Ratio: The Sharpe ratio of {sharpe_ratio:.4f} evaluates return in relation to risk. "
            f"A higher Sharpe ratio indicates that the achieved return is more attractive relative to the risk."
        )
    
    # Empfehlungen zur Risikominderung
    st.subheader("Risk Mitigation Recommendations:")
    st.write(
        "Investing always involves risks. Here are some recommendations to help mitigate risks and enhance your investment strategy:"
    )
    st.write(
        "1. **Diversification:** Spread your investments across different asset classes (stocks, bonds, real estate) to reduce concentration risk."
    )
    st.write(
        "2. **Regular Monitoring:** Stay informed about market trends and regularly review your investment portfolio to make timely adjustments."
    )
    st.write(
        "3. **Risk Tolerance:** Assess your risk tolerance before making investment decisions. Only invest what you can afford to lose."
    )
    st.write(
        "4. **Long-Term Perspective:** Consider a long-term investment horizon to ride out short-term market fluctuations."
    )
    st.write(
        "5. **Professional Advice:** Consult with a financial advisor to get personalized advice based on your financial goals and risk profile."
    )
   
# Loan calculator page content:
def loan_calculator_page():
    st.subheader("Loan Calculator")

    # User inputs
    loan_amount = st.number_input("Loan Amount:", min_value=0.0, step=100.0)
    interest_rate = st.slider("Interest Rate (%)", 0.0, 20.0, 5.0)
    loan_term = st.slider("Loan Term (Years)", 1, 30, 15)

    if st.button("Calculate"):
        #Define monthly_interest_rate within the button click block
        monthly_interest_rate = (interest_rate / 100) / 12

        monthly_payment, total_cost, total_interest = calculate_loan_payment(loan_amount, interest_rate, loan_term, monthly_interest_rate)

        # Display results
        st.write(f"Your monthly loan payment is: {monthly_payment:.2f} EUR")
        st.write(f"Total Cost of the Loan: {total_cost:.2f} EUR")
        st.write(f"Total Interest Paid: {total_interest:.2f} EUR")

        # Chart for illustration
        chart_data = {"Principal": [], "Interest": []}
        remaining_principal = loan_amount
        for _ in range(loan_term * 12):
            interest_payment = remaining_principal * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            remaining_principal -= principal_payment
            chart_data["Principal"].append(principal_payment)
            chart_data["Interest"].append(interest_payment)

        chart_df = pd.DataFrame(chart_data)
        st.area_chart(chart_df, use_container_width=True, color=['#ADD8E6', '#FFA07A'])

        # Interpretation
        st.subheader("Loan Interpretation:")
        st.write(
            f"The chart illustrates the monthly breakdown of principal (orange) and interest (gray) payments over the {loan_term} years loan term."
            f"The x-axis represents time in months, and the y-axis represents the amount in EUR."
            f"The orange area represents the portion of your payment going towards repaying the borrowed amount (Principal), while the gray area represents the interest charged by the lender."
            f"This visualization helps you understand how your payments contribute to the overall cost of the loan."
        )

    #Recommendations
        st.subheader("Loan Recommendations:")
        st.write(
            "1. **Budget Planning:** Ensure that the monthly payment fits within your budget to avoid financial strain.\n"
            "2. **Compare Offers:** Shop around and compare loan offers from different lenders to get the best terms.\n"
            "3. **Early Payments:** Consider making extra payments to reduce the total interest paid over the loan term."
        )

# Function to calculate loan payment details
def calculate_loan_payment(loan_amount, interest_rate, loan_term, monthly_interest_rate):
      # Calculate the total number of payments
    num_payments = loan_term * 12
    # Calculate the monthly payment using the formula for an amortizing loan
    monthly_payment = (
        loan_amount
        * monthly_interest_rate
        * (1 + monthly_interest_rate) ** num_payments
    ) / ((1 + monthly_interest_rate) ** num_payments - 1)
# Calculate the total cost of the loan
    total_cost = monthly_payment * num_payments
   # Calculate the total interest paid
    total_interest = total_cost - loan_amount
 # Return the calculated values
    return monthly_payment, total_cost, total_interest

# Function for the "Contact Us" page
def contact_page():

 # Display contact information
    st.subheader("Contact Us")
    st.write(
        "Do you have any questions, suggestions, or concerns? We're here to help! "
        "Feel free to reach out to us through the following channels:"
    )

    # Display contact information including email, phone, and address
    st.markdown(
        """
        - **Email:** [info@financebuddy.com](mailto:info@financebuddy.com)
        - **Phone:** +1 (123) 456-7890
        - **Address:** 123 Finance Street, Berlin, Germany
        """
    )
# Entry point of the application
if __name__ == "__main__":
# Entry point of the application
    main()