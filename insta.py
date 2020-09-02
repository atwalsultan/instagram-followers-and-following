import os
from time import sleep
from selenium import webdriver

class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://instagram.com')
        sleep(5)


    def login(self):
        # Get username and password for Instagram account
        username = os.environ.get('INSTA_USER') # Put username here
        password = os.environ.get('INSTA_PASS') # Put password here

        self.username = username

        # Login
        self.driver.find_element_by_xpath('//input[@name=\"username\"]').send_keys(username)
        self.driver.find_element_by_xpath('//input[@name=\"password\"]').send_keys(password)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(5)
        return


    def get_followers_and_following(self):
        # Get rid of dialog boxes on home page
        self.driver.find_element_by_xpath('//button[text()="Not Now"]').click()
        sleep(2)
        self.driver.find_element_by_xpath('//button[text()="Not Now"]').click()
        sleep(2)

        # Visit profile page
        self.driver.find_element_by_xpath('//a[contains(@href,"/{}")]'.format(self.username)).click()
        sleep(5)

        # Get following
        self.driver.find_element_by_xpath('//a[contains(@href,"/following")]').click()
        sleep(2)
        following = self._usernames()

        # Get followers
        self.driver.find_element_by_xpath('//a[contains(@href,"/followers")]').click()
        sleep(2)
        followers = self._usernames()

        # Usernames that don't follow you
        not_following_me = [username for username in following if username not in followers]

        # Usernames that you don't follow
        me_not_following = [username for username in followers if username not in following]

        # Print results
        print("Usernames of people who don't follow you back:")
        print('----------------------------------------------------------------------')
        print(not_following_me)
        print()

        print("Usernames of people that you don't follow back:")
        print('----------------------------------------------------------------------')
        print(me_not_following)
        print()


    def _usernames(self):
        # Get modal displaying following/followers
        modal = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')

        # Scroll to the end of the list in modal
        last, current = 0, 1
        while last!=current:
            last = current
            sleep(2)
            current = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
            """, modal)

        # All users in the modal list
        users = modal.find_elements_by_tag_name('a')

        # Usernames of all users
        names = [username.text for username in users if username.text != '']

        # Close modal
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()

        return names

    
    def logout(self):
        # Logout
        # self.driver.find_element_by_xpath('//img[@data-testid="user-avatar"]').click()
        self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img').click()
        sleep(1)
        self.driver.find_element_by_xpath('//div[text()="Log Out"]').click()
        sleep(5)
        self.driver.quit()


# Initialize bot
insta_bot = Bot()

# Log in to Instagram account
insta_bot.login()

# Print users who don't follow you and those who you don't follow
insta_bot.get_followers_and_following()

# Log out of Instagram account
insta_bot.logout()
