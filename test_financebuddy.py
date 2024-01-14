import numpy as np
import pytest

from StreamlitApp import (
    calculate_months_to_goal,
    calculate_budget_per_person,
    calculate_volatility,
    calculate_sharpe_ratio,
)

# Test function for calculate_months_to_goal
@pytest.mark.parametrize("savings, savings_goal, expected_months", [
    (1000, 5000, 5),
    (2000, 10000, 5),
    (0, 1000, float('inf')),
])
def test_calculate_months_to_goal(savings, savings_goal, expected_months):
    # Calculate the result using the function
    result = calculate_months_to_goal(savings, savings_goal)
    
    # Assert that the result matches the expected value
    assert result == expected_months

# Test function for calculate_budget_per_person
@pytest.mark.parametrize("monthly_expenses, num_people, expected_budget", [
    (1000, 2, 500),
    (1500, 3, 500),
    (0, 1, 0),
])
def test_calculate_budget_per_person(monthly_expenses, num_people, expected_budget):
    # Calculate the result using the function
    result = calculate_budget_per_person(monthly_expenses, num_people)
    
    # Assert that the result matches the expected value
    assert result == expected_budget

# Test function for calculate_volatility
def test_calculate_volatility():
    # Sample returns data
    returns = [0.02, 0.05, -0.03, 0.01, 0.03]
    
    # Calculate the result using the function
    result = calculate_volatility(returns)
    
    # Calculate the expected value using numpy's std function
    expected = np.std(returns)
    
    # Assert that the result matches the expected value using pytest.approx
    assert result == pytest.approx(expected)

# Test function for calculate_sharpe_ratio
def test_calculate_sharpe_ratio():
    # Sample returns data
    returns = [0.02, 0.05, -0.03, 0.01, 0.03]
    
    # Calculate the result using the function
    result = calculate_sharpe_ratio(returns)
    
    # Calculate the expected Sharpe ratio manually
    average_return = np.mean(returns)
    volatility = np.std(returns)
    risk_free_rate = 0.01
    expected = (average_return - risk_free_rate) / volatility if volatility != 0 else 0
    
    # Assert that the result matches the expected value using pytest.approx
    assert result == pytest.approx(expected)
