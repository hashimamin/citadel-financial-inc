import pytest
import pyrebase
from app import app
import json

@pytest.fixture
def test_client():
    return app.test_client()


def test_print_account_checking_balance(test_client):
    response = test_client.get("/accounts?uid=nligsz1JQcXTlys08mO8qup7HZo2")
    assert response.status_code == 200
    assert response.json["checking"]["balance"] == 0


def test_print_account_savings_balance(test_client):
    response = test_client.get("/accounts?uid=nligsz1JQcXTlys08mO8qup7HZo2")
    assert response.status_code == 200
    assert response.json["savings"]["balance"] == 0


def test_withdraw_money_from_checking_less_than_balance(test_client):
    test_client.post("/account/checking/deposit",
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                           "amount": 200}),
                     content_type="application/json")

    response = test_client.post("/account/checking/withdraw", 
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100}),
                                content_type="application/json")

    test_client.post("/account/checking/withdraw", 
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                           "amount": 100}),
                     content_type="application/json")
    assert response.status_code == 200
    assert "Withdrawal Successful" in response.get_data(as_text=True)


def test_withdraw_money_from_savings_less_than_balance(test_client):
    test_client.post("/account/savings/deposit",
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                           "amount": 200}),
                     content_type="application/json")

    response = test_client.post("/account/savings/withdraw", 
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100}),
                                content_type="application/json")

    test_client.post("/account/savings/withdraw", 
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                           "amount": 100}),
                     content_type="application/json")
    assert response.status_code == 200
    assert "Withdrawal Successful" in response.get_data(as_text=True)


def test_withdraw_money_from_checking_more_than_balance(test_client):
    response = test_client.post("/account/checking/withdraw", 
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100}),
                                content_type="application/json")

    assert response.status_code == 400
    assert "Withdrawal Unsucessful. Withdrawal amount exceeds account balance." in response.get_data(as_text=True)


def test_withdraw_money_from_savings_more_than_balance(test_client):
    response = test_client.post("/account/savings/withdraw", 
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100}),
                                content_type="application/json")

    assert response.status_code == 400
    assert "Withdrawal Unsucessful. Withdrawal amount exceeds account balance." in response.get_data(as_text=True)


def test_withdraw_money_from_checking_negative_amount(test_client):
    response = test_client.post("/account/checking/withdraw", 
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": -100}),
                                content_type="application/json")

    assert response.status_code == 400
    assert "Withdraw Unsuccessful. Cannot withdraw a negative amount of money." in response.get_data(as_text=True)


def test_withdraw_money_from_savings_negative_amount(test_client):
    response = test_client.post("/account/savings/withdraw", 
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": -100}),
                                content_type="application/json")

    assert response.status_code == 400
    assert "Withdraw Unsuccessful. Cannot withdraw a negative amount of money." in response.get_data(as_text=True)


def test_deposit_money_to_checking(test_client):
    response = test_client.post("/account/checking/deposit",
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                                 "amount": 100}),
                                content_type="application/json")

    test_client.post("/account/checking/withdraw", 
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100}),
                     content_type="application/json")
    assert response.status_code == 200
    assert "Deposit Successful" in response.get_data(as_text=True)


def test_deposit_money_to_savings(test_client):
    response = test_client.post("/account/savings/deposit",
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                                 "amount": 100}),
                                content_type="application/json")

    test_client.post("/account/savings/withdraw", 
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100}),
                     content_type="application/json")
    assert response.status_code == 200
    assert "Deposit Successful" in response.get_data(as_text=True)


def test_transfer_money_checking_to_savings(test_client):
    test_client.post("/account/checking/deposit",
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                           "amount": 100}),
                     content_type="application/json")

    response = test_client.post("/account/checking/transfer",
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                                 "amount": 100,
                                                 "to_acct": "savings"}),
                                content_type="application/json")

    test_client.post("/account/savings/withdraw", 
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100}),
                     content_type="application/json")
    assert response.status_code == 200
    assert "Transfer Successful" in response.get_data(as_text=True)


def test_transfer_money_savings_to_checking(test_client):
    test_client.post("/account/savings/deposit",
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                           "amount": 100}),
                     content_type="application/json")

    response = test_client.post("/account/savings/transfer",
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                                 "amount": 100,
                                                 "to_acct": "checking"}),
                                content_type="application/json")

    test_client.post("/account/checking/withdraw", 
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100}),
                     content_type="application/json")
    assert response.status_code == 200
    assert "Transfer Successful" in response.get_data(as_text=True)


def test_transfer_money_checking_to_savings_negative_amount(test_client):
    response = test_client.post("/account/checking/transfer",
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                                 "amount": -100,
                                                 "to_acct": "savings"}),
                                content_type="application/json")

    assert response.status_code == 400
    assert "Transfer Unsuccessful. Transfer amount cannot be negative" in response.get_data(as_text=True)


def test_transfer_money_savings_to_checkings_negative_amount(test_client):
    response = test_client.post("/account/savings/transfer",
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                                 "amount": -100,
                                                 "to_acct": "checking"}),
                                content_type="application/json")
                                
    assert response.status_code == 400
    assert "Transfer Unsuccessful. Transfer amount cannot be negative" in response.get_data(as_text=True)


def test_transfer_money_checking_to_savings_greater_than_balance(test_client):
    response = test_client.post("/account/checking/transfer",
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                                 "amount": 100,
                                                 "to_acct": "savings"}),
                                content_type="application/json")

    assert response.status_code == 400
    assert "Transfer Unsucessful. Transfer amount exceeds origin account balance." in response.get_data(as_text=True)


def test_transfer_money_savings_to_checking_greater_than_balance(test_client):
    response = test_client.post("/account/savings/transfer",
                                data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                                 "amount": 100,
                                                 "to_acct": "checking"}),
                                content_type="application/json")

    assert response.status_code == 400
    assert "Transfer Unsucessful. Transfer amount exceeds origin account balance." in response.get_data(as_text=True)


def test_transaction_record_creation_when_transaction_occurs(test_client):
    response1 = test_client.get("/transactions/checking?uid=nligsz1JQcXTlys08mO8qup7HZo2")
    
    test_client.post("/account/checking/deposit",
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100}),
                     content_type="application/json")

    response2 = test_client.get("/transactions/checking?uid=nligsz1JQcXTlys08mO8qup7HZo2")

    test_client.post("/account/checking/withdraw", 
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100}),
                     content_type="application/json")

    assert response2.status_code == 200
    assert len(response2.json.keys()) == (len(response1.json.keys()) + 1)


def test_payment_from_checking_equal_to_balance(test_client):
    test_client.post("/account/checking/deposit", 
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100}),
                     content_type="application/json")

    response = test_client.post("/account/checking/payment",
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100,
                                      "to_acct": "ETSY Seller #1234"}),
                     content_type="application/json")

    assert response.status_code == 200
    assert "Payment Successful" in response.get_data(as_text=True)


def test_payment_from_savings_equal_to_balance(test_client):
    test_client.post("/account/savings/deposit", 
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100}),
                     content_type="application/json")

    response = test_client.post("/account/savings/payment",
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100,
                                      "to_acct": "ETSY Seller #1234"}),
                     content_type="application/json")

    assert response.status_code == 200
    assert "Payment Successful" in response.get_data(as_text=True)


def test_payment_from_checking_greater_than_balance(test_client):
    response = test_client.post("/account/checking/payment",
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100,
                                      "to_acct": "ETSY Seller #1234"}),
                     content_type="application/json")

    assert response.status_code == 400
    assert "Payment Unsucessful. Payment amount exceeds account balance." in response.get_data(as_text=True)


def test_payment_from_savings_greater_than_balance(test_client):
    response = test_client.post("/account/savings/payment",
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": 100,
                                      "to_acct": "ETSY Seller #1234"}),
                     content_type="application/json")

    assert response.status_code == 400
    assert "Payment Unsucessful. Payment amount exceeds account balance." in response.get_data(as_text=True)


def test_payment_from_checking_negative_amount(test_client):
    response = test_client.post("/account/checking/payment",
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": -100,
                                      "to_acct": "ETSY Seller #1234"}),
                     content_type="application/json")

    assert response.status_code == 400
    assert "Payment Unsucessful. Payment amount cannot be negative." in response.get_data(as_text=True)


def test_payment_from_savings_negative_amount(test_client):
    response = test_client.post("/account/savings/payment",
                     data=json.dumps({"uid": "nligsz1JQcXTlys08mO8qup7HZo2",
                                      "amount": -100,
                                      "to_acct": "ETSY Seller #1234"}),
                     content_type="application/json")

    assert response.status_code == 400
    assert "Payment Unsucessful. Payment amount cannot be negative." in response.get_data(as_text=True)
