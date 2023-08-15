from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as exp_con
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint

# *********************************X-PATH Locators**********************************
sign_up_locator='//*[contains(@href, "signup")]'
alert_box = '//div[@class = "MuiAlert-message"][contains(text(), invalid)]'
home_page_sidebar = '//span[text()="{}"]'
submit_locator='//button[@type = "submit"]'
onboard_header = '//div[contains(@data-test, "title")]/h2'
sign_in_rem_me = '//*[@name="remember"][@type="checkbox"]'
sign_in_dialog_next = '//button/span[text()= "{}"]'
bank_acc_nav = '//*[@href = "/bankaccounts"]'
bank_acc_create = '//*[@href="/bankaccounts/new"]'
verify_bank_acc = '//*[@class = "MuiList-root MuiList-padding"][@data-test = "bankaccount-list"]/descendant::*[contains(p, "{}")]'
delete_bank_acc = '//*[@class = "MuiList-root MuiList-padding"][@data-test = "bankaccount-list"]/descendant::*[contains(p, "{}")]/following-sibling::*/button[contains(span,"Delete")]'
new_transaction = '//a[@href = "/transaction/new"]'
contact = '//span[text() = "Edgar Johns"]'
multi_submit = '//button[@type = "submit"]/span[text() = "{}"]'
transaction_pane = '//a/span[text() = "Everyone"]'
notify = '//a[@href = "/notifications"]'
dismiss = '//button/span[text()= "Dismiss"]'
transaction_list = '//div[@data-test = "transaction-list"]/div/div/div'
transaction_like = '//button[contains(@data-test, "transaction-like-button")]'
transaction_like_disabled = '//button[contains(@data-test, "transaction-like-button")][contains(@class , "disabled")]'
transaction_like_count = '//div[contains(@data-test, "transaction-like-count")]'
comment_box = '//input[contains(@id , "transaction-comment-input")]'
comment_header = '//h2[contains(text(),"Comment")]'
comment_list = '//h2[contains(text(),"Comment")]/following-sibling::*/li'

#*******************************************************************************************************************

class cypress_automation:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def setup(self):
        ''' Setup - Navigates to the URL
        '''
        self.driver.get('http://localhost:3000/')

    def teardown(self):
        ''' Teardown - Quits the intiated webdriver
        '''
        self.driver.quit()

    def navigate_sign_up(self):
        '''Navigates To SignUp

        '''
        self.driver.find_element(By.XPATH, sign_up_locator).click()  # clicks the Sign up link
        print('Sign Up Clicked!!')
        WebDriverWait(self.driver, 5).until(
            exp_con.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'Sign Up'))  # Verifies the header is Sign Up
        print(f'Navigated to Sign Up page!!')

    def sign_in(self):
        ''' Verifies the Sign In Page navigated or Not

        '''
        WebDriverWait(self.driver, 5).until(exp_con.text_to_be_present_in_element((By.TAG_NAME, 'h1'),
                                                                                  'Sign in'))  # verifies it returns to the Sign in page after Sign Up
        print('Navigated to SignIn Page')

    def sign_in_verify(self):
        ''' Verifies navigated to Home page after Sign In

        '''
        try:
            # Onboarding script
            data = self.driver.find_element(By.XPATH, onboard_header).text
            assert 'Get Started with Real World App' in data
            text_boxes = {'bankName': 'HDFC6', 'routingNumber': '123456789', 'accountNumber': 'IYT17374889'}
            self.driver.find_element(By.XPATH, sign_in_dialog_next.format('Next')).click()
            self.create_bank_account(text_boxes)
            if exp_con.title_is('Finished'):
                self.driver.find_element(By.XPATH, sign_in_dialog_next.format('Done')).click()
            print(f'Signed In after onboard')
        except NoSuchElementException:
            self.driver.find_element(By.XPATH, home_page_sidebar.format('Home'))
            print(f'Signed In')

    def sign_in_alert_box(self):
        ''' Verifies Invalid alert box is received or not

        '''
        assert 'invalid' in self.driver.find_element(By.XPATH, alert_box).text
        print(f'Invalid Login!!')

    def log_out_clicked(self):
        ''' Clicks the logout element

        '''
        self.driver.find_element(By.XPATH, home_page_sidebar.format('Logout')).click()
        print('Logout is clicked')

    def bank_acc_nav(self):
        ''' Navigates to bank profile page

        '''
        self.driver.find_element(By.XPATH, bank_acc_nav).click()
        assert 'Bank Accounts' in self.driver.find_element(By.TAG_NAME, 'h2').text
        self.driver.find_element(By.XPATH, bank_acc_create).click()
        print('Navigated To Bank Profile')

    def bank_acc_verification(self,bank_name):
        ''' Verifies the bank account details added or not

        Args:
            bank_name: Added Bank Name

        '''
        account_name = self.driver.find_element(By.XPATH, verify_bank_acc.format(bank_name)).text
        assert bank_name == account_name
        print(f'Bank Account Created - {account_name}')

    def delete_acc(self,bank_name):
        ''' Deletes the Bank Account

        Args:
            bank_name: Bank name needs to deleted
        '''
        self.driver.find_element(By.XPATH, delete_bank_acc.format(bank_name)).click()
        print(f'Delete {bank_name} initiated')

    def verify_del_acc(self,bank_name):
        ''' Verifies the Bank Account is deleted

        Args:
            bank_name: Bank name needs to deleted
        '''
        assert exp_con.presence_of_element_located(verify_bank_acc.format(f"{bank_name} (Deleted)"))
        print('Bank account deleted')

    def navigate_bank_profile(self):
        ''' Navigates to Bank Profile page

        '''
        self.driver.find_element(By.XPATH, bank_acc_nav).click()
        assert 'Bank Accounts' in self.driver.find_element(By.TAG_NAME, 'h2').text
        print('Navigated to Bank Profile page')

    def navigate_transaction(self,text_boxes):
        ''' Navigates to Transaction Page

        Args:
            text_boxes: Sign In Details in dict
        '''
        self.navigate_to_homepage(text_boxes)
        self.driver.find_element(By.XPATH, new_transaction).click()

    def select_contact(self):
        ''' Selects the contact

        '''
        self.driver.find_element(By.XPATH, contact).click()
        assert "Edgar Johns" in self.driver.find_element(By.TAG_NAME, 'h2').text

    def payment_done(self,text_boxes,mode):
        ''' Intiates the Transactions (Pay/Request)

        Args:
            text_boxes: Transaction details in dict
            mode: Pay/Request

        '''
        for label, data in text_boxes.items():
            element = self.driver.find_element(By.ID, label)
            if element.get_attribute('value'):
                element.clear()
            element.send_keys(data)
            sleep(1)
        print(f'Data Updated!!')
        self.driver.find_element(By.XPATH, multi_submit.format(mode)).click()

    def payment_verified(self, mode):
        ''' Verifies the Transaction mode

        Args:
            mode: Pay/Request

        '''
        assert mode in self.driver.find_element(By.XPATH, f'//h2[contains(text(), "{mode}")]').text

    def navigate_notification_page(self,text_boxes):
        ''' Navigates To Notification Page

        Args:
            text_boxes: Sign In details

        '''
        self.navigate_to_homepage(text_boxes)
        self.driver.find_element(By.XPATH, notify).click()
        assert "Notifications" in self.driver.find_element(By.TAG_NAME, 'h2').text

    def clear_notification(self):
        ''' Clears all notification

        '''
        notify_count = self.driver.find_elements(By.XPATH, dismiss)
        if len(notify_count) > 0:
            for index in range(len(notify_count)):
                notify_count[index].click()
        else:
            print('No Notifications')

    def cleared_notify(self):
        ''' Verifies the Notifications are cleared

        '''
        data = self.driver.find_element(By.TAG_NAME, 'h2').text
        print(data)
        assert "No Notifications" in self.driver.find_element(By.XPATH, '//h2[contains(text(), "No ")]').text

    def navigate_trans_list(self,text_boxes):
        ''' Navigates to Transaction list page

        Args:
            text_boxes: Sign In Details

        '''
        self.navigate_to_homepage(text_boxes)
        self.driver.find_element(By.XPATH, home_page_sidebar.format('Home')).click()
        self.driver.find_element(By.XPATH, transaction_pane).click()

    def select_transaction(self):
        ''' Selects the random Transactions from the list

        '''
        trans_list = self.driver.find_elements(By.XPATH, transaction_list)
        index = randint(1, len(trans_list))
        print(f'index - {index}')
        self.driver.find_element(By.XPATH, transaction_list + f'[{index}]').click()
        sleep(2)
        assert "Transaction Detail" in self.driver.find_element(By.TAG_NAME, 'h2').text

    def click_like(self):
        ''' Selcts the Like Button

        '''
        if not 'disabled' in self.driver.find_element(By.XPATH, transaction_like).get_attribute('class'):
            count = int(self.driver.find_element(By.XPATH, transaction_like_count).text)
            self.cnt = count
            print(f'count {self.cnt}')
            sleep(1)
            self.driver.find_element(By.XPATH, transaction_like).click()
        else:
            print('Like Button Disabled')

    def like_added(self):
        ''' Verifies the like counted

        '''
        assert str(self.cnt + 1) in self.driver.find_element(By.XPATH, transaction_like_count).text

    def comment(self,comment):
        ''' Comments added

        Args:
            comment: comment needs to be added

        '''
        com_element = self.driver.find_element(By.XPATH, comment_box)
        com_element.send_keys(comment)
        com_element.send_keys(Keys.ENTER)
        sleep(1)
        assert "Comments" in self.driver.find_element(By.XPATH, comment_header).text

    def comment_verified(self,comment):
        ''' Verifies the added comment
        Args:
            comment: Comment added

        '''
        com_list = len(self.driver.find_elements(By.XPATH, comment_list))
        assert comment in self.driver.find_element(By.XPATH, comment_list + f'[{com_list}]//span').text

    def submit(self):
        ''' Click Submit Button

        '''
        end = self.driver.find_element(By.XPATH, submit_locator)
        if end.is_enabled():
            end.submit()
            sleep(2)
        else:
            print('Failed!! - Submit is Disabled')

    def update_values(self,text_boxes):
        ''' Updates the provided data in text boxes

        Args:
            text_boxes: Data to be updated

        '''
        print(text_boxes)
        for label, data in text_boxes.items():
            element = self.driver.find_element(By.ID, label)
            if element.get_attribute('value'):
                element.clear()
            element.send_keys(data)
            sleep(1)
        print(f'Data Updated!!')
        self.submit()

    def navigate_to_homepage(self,text_boxes):
        ''' Navigates to Home Page

        Args:
            text_boxes: Sign in details

        '''
        WebDriverWait(self.driver, 5).until(exp_con.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'Sign in'))  # Verifies the header is Sign In
        self.update_values(text_boxes)
        assert exp_con.presence_of_element_located(home_page_sidebar.format('Home'))

    def create_bank_account(self,text_data):
        ''' Create the bank account

        Args:
            text_data: Bank details needs to be added

        '''
        assert 'Create Bank Account' in self.driver.find_element(By.TAG_NAME, 'h2').text
        for label, data in text_data.items():
            element = self.driver.find_element(By.NAME, label)
            if element.get_attribute('value'):
                element.clear()
            element.send_keys(data)
            sleep(1)
        self.submit()
