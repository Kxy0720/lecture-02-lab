from app.schema import ExpressionIn
# Import from the new location
from app.dependencies import expand_percent 

def test_expand_percent():
    request_data = ExpressionIn(expr="5 + 10%") # creating the Pydantic object
    assert expand_percent(request_data) == "5 + ((10/100)*5)", (
        f"Expected '5 + ((10/100)*5)', got {expand_percent(request_data)}" # passing the Pydantic object to the function
    )

    request_data = ExpressionIn(expr="20 - 30%") 
    assert expand_percent(request_data) == "20 - ((30/100)*20)", (
        f"Expected '20 - ((30/100)*20)', got {expand_percent(request_data)}"
    )

    request_data = ExpressionIn(expr="15 * 25%") 
    assert expand_percent(request_data) == "15 * (25/100)", (
        f"Expected '15 * (25/100)', got {expand_percent(request_data)}"
    )

    request_data = ExpressionIn(expr="40 / 50%") 
    assert expand_percent(request_data) == "40 / (50/100)", (
        f"Expected '40 / (50/100)', got {expand_percent(request_data)}"
    )

    request_data = ExpressionIn(expr="3 * 4% + 2 / 1%") 
    assert expand_percent(request_data) == "3 * (4/100) + 2 / (1/100)", (
        f"Expected '3 * (4/100) + 2 / (1/100)', got {expand_percent(request_data)}"
    )

    request_data = ExpressionIn(expr="100%") 
    assert expand_percent(request_data) == "(100/100)", (
        f"Expected '(100/100)', got {expand_percent(request_data)}"
    )

    request_data = ExpressionIn(expr="10% + 20%") 
    assert expand_percent(request_data) == "(10/100) + (20/100)", (
        f"Expected '(10/100) + (20/100)', got {expand_percent(request_data)}"
    )

if __name__ == "__main__":
    test_expand_percent()
    print("All tests passed!")