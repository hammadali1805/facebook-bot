from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import os
import re 

def login(driver, email, password):
    """
    Logs into Facebook with provided credentials.

    Args:
    - driver: Selenium WebDriver instance.
    - eamil: Facebook email.
    - password: Facebook password.
    - phone: Phone Number added in Facebook.

    Returns:
    - True if login successful, False otherwise.
    """

    try:
        driver.get("https://www.facebook.com/")
        time.sleep(1)
        
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "pass")
        
        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        
        time.sleep(3)
        print(driver.current_url)
        if driver.current_url == "https://www.facebook.com/":                
            return True

    except Exception as e:
        print(f"Error during login: {str(e)}")
        return False





def logout(driver):
    """
    Logs out from Facebook.

    Args:
    - driver: Selenium WebDriver instance.
    """
    try:
        driver.get('https://www.facebook.com/')
        time.sleep(1)
        # Logout
        account_button = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Your profile"]')
        account_button.click()
        time.sleep(1)

        logout_button_path = "/html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div[1]/div[2]/div/div[5]/div"
        logout_button = driver.find_element(By.XPATH, logout_button_path)
        logout_button.click()

        # Wait for logout to complete
        time.sleep(3)

    except Exception as e:
        print(f"Error during logout: {str(e)}")


def react_post(driver, post_url):
    # Like, Love, Care, Haha, Wow, Sad, Angry
    try:
        driver.get(post_url)
        time.sleep(2)
        
        # if reaction=='Like':
        #     like_button = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Like"]')
        #     like_button.click()
        # else:
        #     driver.find_element(By.CSS_SELECTOR, 'div[aria-label="React"]').click()
        #     time.sleep(1)
            # driver.find_element(By.CSS_SELECTOR, f'div[aria-label="{reaction}"]').click()

        driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Like"]').click()
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error while liking post: {str(e)}")
        return False


def checkMember(driver, group_link):
    """
    Checks if the loggedin user is the member of the specified group.

    Args:
    - driver: Selenium WebDriver instance.
    - group_link: URL of the group.

    Returns:
    - True if member, False otherwise.
    """
    driver.get(group_link)
    time.sleep(3)
    try:
        driver.find_element(By.XPATH, "//div[@aria-label='Joined']")
        return True
    except:
        return False
    

def groupMembers(driver, group_link):
    members_url = group_link + "/members"
    driver.get(members_url)
    time.sleep(3)

    members = set()

    while True:
        try:
            member_elements = driver.find_elements(By.XPATH, "//a[@role='link']")
            current_member_count = len(members)

            for member in member_elements:
                try:
                    name = member.text.strip()
                    username = member.get_attribute("href")

                    match = re.search(r'user/(\d+)', username)
                    user_id = match.group(1) if match else None

                    if name and user_id and not re.search(r'\b0 points\b', name, re.IGNORECASE):
                        members.add((name, user_id))

                except StaleElementReferenceException:
                    # If a member element becomes stale, simply continue to the next one
                    continue

            # Scroll down to load more members
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            # Check if new members were found
            new_member_count = len(members)
            if new_member_count == current_member_count:
                print("No new members found. Stopping scroll.")
                break

        except Exception as e:
            print(f"Error finding members: {e}")
            break

    if members:
        names, ids = zip(*members)
        data = {"Name": names, "Id": ids}
        return data
    else:
        return False

# def postMembers(driver, post_link):
#     driver.get(post_link)
#     time.sleep(3)
#     reactions_path = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div"
#     driver.find_elements(By.XPATH, reactions_path).click()
#     time.sleep(2)

#     members = set()

#     while True:
#         try:
#             member_elements = driver.find_elements(By.XPATH, "//a[@role='link']")
#             current_member_count = len(members)

#             for member in member_elements:
#                 try:
#                     name = member.text.strip()
#                     username = member.get_attribute("href")

#                     match = re.search(r'user/(\d+)', username)
#                     user_id = match.group(1) if match else None

#                     if name and user_id and not re.search(r'\b0 points\b', name, re.IGNORECASE):
#                         members.add((name, user_id))

#                 except StaleElementReferenceException:
#                     # If a member element becomes stale, simply continue to the next one
#                     continue

#             # Scroll down to load more members
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)

#             # Check if new members were found
#             new_member_count = len(members)
#             if new_member_count == current_member_count:
#                 print("No new members found. Stopping scroll.")
#                 break

#         except Exception as e:
#             print(f"Error finding members: {e}")
#             break

#     if members:
#         names, ids = zip(*members)
#         data = {"Name": names, "Id": ids}
#         return data
#     else:
#         return False




def comment_post(driver, post_url, comment_text):
    try:
        driver.get(post_url)
        time.sleep(2)

        driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Leave a comment"]').click()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]').send_keys(comment_text)
        time.sleep(2)

        driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Comment"]').click()

        # Give it some time for the comment to post
        time.sleep(2)
        return True

    except Exception as e:
        print(f"Error while commenting on post: {str(e)}")
        return False


# def report_tweet(driver, tweet_url):
#     """
#     Reports a tweet specified by URL.

#     Args:
#     - driver: Selenium WebDriver instance.
#     - tweet_url: URL of the tweet to report.
#     """
#     try:
#         driver.get(tweet_url)
#         time.sleep(2)  # Let the page load

#         # Click more options button
#         driver.find_element(By.CSS_SELECTOR, 'button[data-testid="caret"]').click()
#         time.sleep(2)  # Wait for options to expand

#         # Click report tweet
#         driver.find_element(By.CSS_SELECTOR, 'div[data-testid="report"]').click()
#         time.sleep(1)  # Wait for report modal to appear

#         options = [
#             '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[1]',
#             '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[2]',
#             '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[3]',
#                    ]
#         selected = random.choice(options)
#         driver.find_element(By.XPATH, selected).click()
#         time.sleep(1)

#         driver.find_element(By.CSS_SELECTOR, '[data-testid="ChoiceSelectionNextButton"]').click()
#         time.sleep(1)

#         next_options = [
#             '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[1]',
#             '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[2]',
#             '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[3]',
#         ]
#         next_selected = random.choice(next_options)
#         driver.find_element(By.XPATH, next_selected).click()
#         time.sleep(1)

#         driver.find_element(By.CSS_SELECTOR, '[data-testid="ChoiceSelectionNextButton"]').click()
#         time.sleep(1)
        
#         return True
#     except Exception as e:
#         print(f"Error while reporting tweet: {str(e)}")
#         return False


def follow_user(driver, user_profile_url):
    try:
        driver.get(user_profile_url)
        time.sleep(2)  # Let the page load

        follow_button = driver.find_element(By.CSS_SELECTOR, f'div[aria-label="Add friend"]')
        follow_button.click()
        time.sleep(2)
        return True
    
    except Exception as e:
        print(f"Error while following user: {str(e)}")
        return False


def message_user(driver, user_profile_url, message_text):
    try:
        driver.get(user_profile_url)
        time.sleep(2)  # Let the page load

        # Click message button
        message_button = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Message"]')
        message_button.click()
        time.sleep(2)

        # Enter message
        message_box = driver.find_element(By.CSS_SELECTOR, 'div[aria-placeholder="Aa"]')
        message_box.send_keys(message_text)
        time.sleep(2)

        # Send message
        send_button = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Press Enter to send"]')
        send_button.click()
        time.sleep(2)
        return True
    
    except Exception as e:
        print(f"Error while messaging user: {str(e)}")
        return True


# def report_user(driver, user_profile_url):
#     """
#     Reports a user specified by profile URL.

#     Args:
#     - driver: Selenium WebDriver instance.
#     - user_profile_url: URL of the user's profile to report.
#     """
#     try:
#         driver.get(user_profile_url)
#         time.sleep(2)  # Let the page load

#         # Click more options button
#         driver.find_element(By.CSS_SELECTOR, 'button[data-testid="userActions"]').click()
#         time.sleep(1)  # Wait for options to expand

#         # Click report tweet
#         driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div[1]/div/div/div[2]/div/div[3]/div/div/div/div[6]').click()
#         time.sleep(2)  # Wait for report modal to appear

#         options = [
#             '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[1]',
#             '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[2]',
#             '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[3]',
#                    ]
#         selected = random.choice(options)
#         driver.find_element(By.XPATH, selected).click()
#         time.sleep(1)

#         driver.find_element(By.CSS_SELECTOR, '[data-testid="ChoiceSelectionNextButton"]').click()
#         time.sleep(1)

#         next_options = [
#             '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[1]',
#             '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[2]',
#             '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[3]',
#         ]
#         next_selected = random.choice(next_options)
#         driver.find_element(By.XPATH, next_selected).click()
#         time.sleep(1)

#         driver.find_element(By.CSS_SELECTOR, '[data-testid="ChoiceSelectionNextButton"]').click()
#         time.sleep(1)
        
#         return True
#     except Exception as e:
#         print(f"Error while reporting tweet: {str(e)}")
#         return False



def find_friends(driver):
    try:
        # Open Twitter login page
        driver.get("https://facebook.com/friends/list")
        time.sleep(2)

        links = set()
        friends = driver.find_elements(By.CSS_SELECTOR, 'a[role="link"]')
        for friend in friends:
            link: str = friend.get_attribute("href")
            if (list(link).count('/') > 3 ) or (link.find('profile.php') != -1) or (link=='https://www.facebook.com/'):
                pass
            else:
                links.add(link)
        
        return links
    
    except Exception as e:
        print(f"Error while finding friends: {str(e)}")
        return False
    

def post(driver, message, folder_path=None):
    try:
        # Open Twitter login page
        driver.get("https://facebook.com")
        time.sleep(2)

        post_box_path = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div"
        # Click on the Tweet button to open the tweet modal
        post_box = driver.find_element(By.XPATH, post_box_path)
        post_box.click()
        time.sleep(5)

        text_box = driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')
        # Type the tweet message
        text_box.send_keys(message)
        time.sleep(1)

        # Check if folder_path is provided, and add a random image if it is
        if folder_path and os.path.exists(folder_path):
            images = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
            if images:
                random_image = os.path.join(folder_path, random.choice(images))
                
                driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Photo/video"]').click()
                time.sleep(1)
                # Find the file input element for image upload and send the file path
                file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
                file_input.send_keys(random_image)
                
                # Allow some time for the image to be processed by Twitter
                time.sleep(3)

        # Post the tweet
        post_button = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Post"]')
        post_button.click()

        # Allow time for the tweet to post
        time.sleep(5)

        return True

    except Exception as e:
        print(f"Error while posting: {str(e)}")
        return False