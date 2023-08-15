*** Settings ***
Library    ./cypress_automation.py    WITH NAME    dev

*** Keywords ***
Setup
    dev.setup

Teardown
    dev.teardown

User Was Navigated To Sign Up Page
    dev.navigate sign up

User Details Are Updated ${user_data}
    dev.update values    ${user_data}

User Should Be Signed Up
    dev.sign in

User Was In Sign In Page
    dev.sign in

User Should Be Signed In
    dev.sign in verify

Invalid Message Should Be Received
    dev.sign in alert box

User Was In Homepage ${user_data}
    dev.navigate to homepage    ${user_data}

User Clicks Logout
    dev.log out clicked

User Should Be Signed Out
    dev.sign in

User Navigates To Bank Account Creation Page
    dev.bank acc nav

User Account Details Are Updated ${user_data}
    dev.create bank account    ${user_data}
    Set Test Variable   ${bank_name}    ${user_data}[bankName]

Bank Account Should Be Created
    dev.bank acc verification    ${bank_name}

User Deletes The Account ${user_data}
    Set Test Variable   ${bank_name}    ${user_data}[bankName]
    dev.delete acc    ${bank_name}

Account Will Be Deleted
    dev.verify del acc    ${bank_name}

User Navigates To Bank Profile Page
    dev.navigate bank profile

User Was In Transaction page ${sign_in_details}
    dev.navigate transaction    ${sign_in_details}

User Selects The Contact
    dev.select contact

Payment Details Updated ${trans_details} And ${mode} Initiated
    dev.payment done    ${trans_details}    ${mode}

Mode ${mode} Should Be Completed
    dev.payment verified    ${mode}

User Was In Notification page ${sign_in_details}
    dev.navigate notification page    ${sign_in_details}

User Clears Notifications
    dev.clear notification

Notifications Should Be Cleared
    dev.cleared notify

User Was In Transaction list page ${sign_in_details}
    dev.navigate trans list    ${sign_in_details}

User Selected Transaction
    dev.select transaction

User Likes The Transaction
    dev.click like

Like Should Be added
    dev.like added

User Comments The Transaction
    Set Test Variable    ${comment}    Comments Added
    dev.comment    ${comment}

Comment Should Be added
    dev.comment verified    ${comment}