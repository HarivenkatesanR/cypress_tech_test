*** Settings ***
Test Setup    Setup
Test Teardown    Teardown
Resource    ./cypress_keywords.robot

*** Variables ***
&{sign_up_details}    firstName=Jiah    lastName=Kumar     username=kiji    password=kiji    confirmPassword=kiji
&{sign_in_details}    username=kiji    password=kiji
&{invalid_sign_in}    username=rtyui    password=tghyuji
&{acc_details}    bankName=HDFC30    routingNumber=123456789    accountNumber=123456789
&{transaction_details}    amount=1000    transaction-create-description-input=Groceries

*** Test Cases ***
Sign UP
    [Tags]    sign_up
    Given User Was Navigated To Sign Up Page
    When User Details Are Updated ${sign_up_details}
    Then User Should Be Signed Up

Sign IN
    [Tags]    sign_in
    Given User Was In Sign In Page
    When User Details Are Updated ${sign_in_details}
    Then User Should Be Signed In

Negative Sign IN
    [Tags]    sign_in_neg
    Given User Was In Sign In Page
    When User Details Are Updated ${invalid_sign_in}
    Then Invalid Message Should Be Received

Logout
    [Tags]    logout
    Given User Was In Homepage ${sign_in_details}
    When User Clicks Logout
    Then User Should Be Signed Out

Add Bank Account
    [Tags]    add_acc
    Given User Was In Homepage ${sign_in_details}
    When User Navigates To Bank Account Creation Page
    And User Account Details Are Updated ${acc_details}
    Then Bank Account Should Be Created

Delete Bank Account
    [Tags]    del_acc
    Given User Was In Homepage ${sign_in_details}
    When User Navigates To Bank Profile Page
    And User Deletes The Account ${acc_details}
    Then Account Will Be Deleted

Transaction Pay
    [Tags]    pay
    Given User Was In Transaction page ${sign_in_details}
    When User Selects The Contact
    And Payment Details Updated ${transaction_details} And Pay Initiated
    Then Mode Paid Should Be Completed

Transaction Request
    [Tags]    request
    Given User Was In Transaction page ${sign_in_details}
    When User Selects The Contact
    And Payment Details Updated ${transaction_details} And Request Initiated
    Then Mode Requested Should Be Completed

Dismiss Notification
    [Tags]    notify
    Given User Was In Notification page ${sign_in_details}
    When User Clears Notifications
    Then Notifications Should Be Cleared

Like Transactions
    [Tags]    like
    Given User Was In Transaction list page ${sign_in_details}
    And User Selected Transaction
    When User Likes The Transaction
    Then Like Should Be added

Comment Transactions
    [Tags]    comment
    Given User Was In Transaction list page ${sign_in_details}
    And User Selected Transaction
    When User Comments The Transaction
    Then Comment Should Be added