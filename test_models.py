import pytest
from app.schema import ExpressionIn
# Import from the new location
from app.dependencies import expand_percent

def test_add_percent():
    # wrapping the dictionary in ExpressionIn
    assert expand_percent(ExpressionIn(expr="5 + 10%")) == "5 + ((10/100)*5)"

def test_subtract_percent():
    assert expand_percent(ExpressionIn(expr="20 - 30%")) == "20 - ((30/100)*20)"

def test_multiply_percent():
    assert expand_percent(ExpressionIn(expr="15 * 25%")) == "15 * (25/100)"

def test_divide_percent():
    assert expand_percent(ExpressionIn(expr="40 / 50%")) == "40 / (50/100)"

def test_multiple_operations():
    assert expand_percent(ExpressionIn(expr="3 * 4% + 2 / 1%")) == "3 * (4/100) + 2 / (1/100)"

def test_standalone_100_percent():
    assert expand_percent(ExpressionIn(expr="100%")) == "(100/100)"

def test_two_standalone_percents():
    assert expand_percent(ExpressionIn(expr="10% + 20%")) == "(10/100) + (20/100)"