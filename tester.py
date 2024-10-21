from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from actions import login, logout, react_post, groupMembers, postMembers, comment_post, follow_user, message_user, post, find_friends
from utils import find_tweets

# Initialize WebDriver
def get_driver():
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

def test_actions(driver):
    # Example usage:
    email = "hammadalipbt18@gmail.com"
    password = ''

    # Login
    if login(driver, email, password):
        try:
            # Example actions
            post_url = "https://www.facebook.com/share/p/sfipcTaZ791peN4W/"
            # user_profile_url = "https://x.com/TheEVuniverse"
            # keyword = "marvel fans"
            # message_text = "Hello!"
            # comment_text = "Hi!"

            # tweets = find_tweets(driver, keyword, 50)
            # print(len(tweets))
            # like_post(driver, post_url)
            print(comment_post(driver, post_url, "Hi!"))
            # data = postMembers(driver, post_url)
            # pd.DataFrame(data).to_csv('members.csv', index=False)
            # retweet_tweet(driver, tweet_url)
            # comment_tweet(driver, tweet_url, comment_text)
            # report_tweet(driver, tweet_url)
            # follow_user(driver, user_profile_url)
            # message_user(driver, user_profile_url, message_text)
            # report_user(driver, user_profile_url)
            print('success')
        finally:
            # Logout
            logout(driver)
    else:
        print("Login failed.")

# Example usage
driver = get_driver()
test_actions(driver)
