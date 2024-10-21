import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from utils import load_csv_file, create_report, get_timestamp, get_filename, get_summary
from actions import *

import google.generativeai as genai
from gemini import paraphrase_content

from tkinter import ttk
from tkinter import filedialog
from selenium.webdriver.chrome.options import Options

from PIL import Image, ImageTk

import pandas as pd

from my_secrets import API_KEY

GOOGLE_API_KEY = API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')



# Initialize WebDriver
def get_driver():
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def perform_action(link, users, action=None, filename=None, comment=None, paraphrase=None, language=None, image_folder=None, swith_after=None):
        
    if len(users)==0:
        messagebox.showerror('Error', 'No CSV selected or empty CSV selected.')
        return
    
    # report_name = get_filename()
    # create_report(['Timestamp', 'PerformedBy', 'Action', 'PerfoedOn', 'Status', 'Comment'], report_name)

    if action=='scrape_users':
        if not filename.strip(' '):
            messagebox.showerror('Error', 'Give a valid filename!')
            return
                    

        if link.startswith('https://www.facebook.com/groups/'):
            driver = get_driver()
            found = False    
            for email, password in users:
                if login(driver, email, password):
                    if checkMember(driver, link):
                        data = groupMembers(driver, link)
                        if data:
                            try:
                                pd.DataFrame(data).to_csv(f'members/{filename}.csv', index=False)
                                messagebox.showinfo('Success', f'Scraped {len(data["Id"])} users.')
                            except Exception as e:
                                messagebox.showerror('Unexpected Error', e)
                        else:
                            messagebox.showerror('Error', 'Unable to scrape users try again!')
                        found = True
                        break
                    else:
                        print(f'{email} is not a member.')
                else:
                    print(f"Login Failed for {email}")
            if not found:
                messagebox.showerror('Error', 'No user from the given csv is the member of the group.')

        elif link.startswith('https://www.facebook.com/share/p/'):
            driver = get_driver()
            for email, password in users:
                if login(driver, email, password):
                    # data = groupMembers(driver, link)
                    data = ''
                    if data:
                        try:
                            pd.DataFrame(data).to_csv(f'members/{filename}.csv', index=False)
                            messagebox.showinfo('Success', f'Scraped {len(data["Id"])} users.')
                        except Exception as e:
                            messagebox.showerror('Unexpected Error', e)
                    else:
                        messagebox.showerror('Error', 'Unable to scrape users try again!')
                    found = True
                    break
                else:
                    print(f"Login Failed for {email}")
        
        else:
            messagebox.showerror('Error', 'Invalid link! link must start with https://www.facebook.com/share/p/ or https://www.facebook.com/groups/')


    if action=='like' or action=='comment':

        if (not link.startswith('https://www.facebook.com/share/p/')):
            messagebox.showerror('Error!', 'Provide proper link. Link should start with https://www.facebook.com/share/p/')
            return 
        
        driver = get_driver()

        report_name = get_filename()
        create_report(['Timestamp', 'PerformedBy', 'Action', 'PostLink', 'Status', 'Comment'], report_name)

        for username, password, phone in users:
            if login(driver, username, password, phone):

                if action == 'like':
                    if react_post(driver, link):
                        create_report([get_timestamp(), username, action, link, 'Success', ''], report_name)
                    else:
                        create_report([get_timestamp(), username, action, link, 'Failed', ''], report_name)

                elif action == 'comment':
                    if paraphrase:

                        new_comment = paraphrase_content(model, comment, language).strip('\n')
                        if new_comment:

                            if comment_post(driver, link, new_comment):
                                create_report([get_timestamp(), username, action, link, 'Success', comment], report_name)
                            else:
                                create_report([get_timestamp(), username, action, link, 'Failed', comment], report_name)
                        else:
                            create_report([get_timestamp(), username, action, link, 'Failed', comment], report_name)

                    else:
                        if comment_post(driver, link, comment):
                            create_report([get_timestamp(), username, action, link, 'Success', comment], report_name)
                        else:
                            create_report([get_timestamp(), username, action, link, 'Failed', comment], report_name)

                logout(driver)
                # time.sleep(delay)
            else:
                create_report([get_timestamp(), username, action, link, 'Failed', ''], report_name)
                
        driver.quit()
        messagebox.showinfo("SUCCESS", f"Automation task has been completed.\n{get_summary(report_name)}")

    # elif task_type=='post':

    #     if login(driver, users[0][0], users[0][1], users[0][2]):
    #         tweets = find_tweets(driver, tweet_link, len(users))
    #         logout(driver)

    #         if tweets:
    #             for tweet, (username, password, phone) in zip(tweets, users):

    #                 if login(driver, username, password, phone):

    #                     if action == 'like':
    #                         if like_tweet(driver, tweet):
    #                             create_report([get_timestamp(), username, action, tweet, 'Sucess', ''], report_name)
    #                         else:
    #                             create_report([get_timestamp(), username, action, tweet, 'Failed',  ''], report_name)


    #                     elif action == 'retweet':                    
    #                         if retweet_tweet(driver, tweet):
    #                             create_report([get_timestamp(), username, action, tweet, 'Success', ''], report_name)
    #                         else:
    #                             create_report([get_timestamp(), username, action, tweet, 'Failed', ''], report_name)



    #                     elif action == 'report':                    
    #                         if report_tweet(driver, tweet):
    #                             create_report([get_timestamp(), username, action, tweet, 'Success', ''], report_name)
    #                         else:
    #                             create_report([get_timestamp(), username, action, tweet, 'Failed', ''], report_name)


    #                     elif action == 'comment':
    #                         if paraphrase:

    #                             new_comment = paraphrase_content(model, comment, language).strip('\n')

    #                             if new_comment:

    #                                 if comment_tweet(driver, tweet, new_comment):
    #                                     create_report([get_timestamp(), username, action, tweet, 'Success', comment], report_name)
    #                                 else:
    #                                     create_report([get_timestamp(), username, action, tweet, 'Failed', comment], report_name)

    #                             else:
    #                                 create_report([get_timestamp(), username, action, tweet, 'Failed', comment], report_name)

    #                         else:

    #                             if comment_tweet(driver, tweet, comment):
    #                                 create_report([get_timestamp(), username, action, tweet, 'Success', comment], report_name)
    #                             else:
    #                                 create_report([get_timestamp(), username, action, tweet, 'Failed', comment], report_name)

    #                     logout(driver)
    #                     time.sleep(delay)
    #                 else:
    #                     create_report([get_timestamp(), username, action, tweet, 'Failed', ''], report_name)
    #         else:
    #             messagebox.showerror("Error", 'Unable to fetch tweets related to post. Please try again.')
    #     else:
    #         messagebox.showerror("Error", 'Unable to fetch tweets related to post. Please try again.')

    # elif task_type=='account':

    #     for username, password, phone in users:
    #         if login(driver, username, password, phone):

    #             if action == 'follow':
    #                 if follow_user(driver, tweet_link):
    #                     create_report([get_timestamp(), username, action, tweet_link, 'Success', ''], report_name)
    #                 else:
    #                     create_report([get_timestamp(), username, action, tweet_link, 'Failed', ''], report_name)


    #             elif action == 'report':                    
    #                 if report_user(driver, tweet_link):
    #                     create_report([get_timestamp(), username, action, tweet_link, 'Success', ''], report_name)
    #                 else:
    #                     create_report([get_timestamp(), username, action, tweet_link, 'Failed', ''], report_name)


    #             elif action == 'message':
    #                 if paraphrase:
    #                     new_comment = paraphrase_content(model, comment, language).strip('\n')

    #                     if new_comment:
                            
    #                         if message_user(driver, tweet_link, new_comment):
    #                             create_report([get_timestamp(), username, action, tweet_link, 'Success', comment], report_name)
    #                         else:
    #                             create_report([get_timestamp(), username, action, tweet_link, 'Failed', comment], report_name)

    #                     else:
    #                         create_report([get_timestamp(), username, action, tweet_link, 'Failed', comment], report_name)

    #                 else:
    #                     if message_user(driver, tweet_link, comment):
    #                         create_report([get_timestamp(), username, action, tweet_link, 'Success', comment], report_name)
    #                     else:
    #                         create_report([get_timestamp(), username, action, tweet_link, 'Failed', comment], report_name)

    #             logout(driver)
    #             time.sleep(delay)
    #         else:
    #             create_report([get_timestamp(), username, action, tweet_link, 'Failed', ''], report_name)



    elif action=='post':

        if (not image_folder) and (not comment.strip(' ')):
            messagebox.showerror('Error!', 'Provide atleast one thing message or images.')
            return 
        
        driver = get_driver()

        report_name = get_filename()
        create_report(['Timestamp', 'PerformedBy', 'Action', 'ImageFolder', 'Status', 'Comment'], report_name)

        for email, password in users:
            if login(driver, email, password):

                if paraphrase:
                    new_comment = paraphrase_content(model, comment, language).strip('\n')

                    if new_comment:
                        
                        if post(driver, new_comment, image_folder):
                            create_report([get_timestamp(), email, action, str(image_folder), 'Success', comment], report_name)
                        else:
                            create_report([get_timestamp(), email, action, str(image_folder), 'Failed', comment], report_name)
                    else:
                        create_report([get_timestamp(), email, action, str(image_folder), 'Failed', comment], report_name)

                else:
                    if post(driver, comment, image_folder):
                        create_report([get_timestamp(), email, action, str(image_folder), 'Success', comment], report_name)
                    else:
                        create_report([get_timestamp(), email, action, str(image_folder), 'Failed', comment], report_name)

                logout(driver)
                # time.sleep(delay)
            else:
                create_report([get_timestamp(), email, action, str(image_folder), 'Failed', comment], report_name)        

        driver.quit()
        messagebox.showinfo("SUCCESS", f"Automation task has been completed.\n{get_summary(report_name)}")

# Main Application Class
class XAutomationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Facebook Automation Tool")
        self.geometry("800x500")
        self.configure(bg="#1DA1F2")  # Twitter blue background

        # Set the Twitter logo as favicon
        self.iconbitmap('facebook.ico')  # Change to your actual Twitter logo path

        # Twitter Logo
        logo = Image.open("facebook.png")  # Change to your actual Twitter logo path
        logo = logo.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(logo)
        logo_label = ttk.Label(self, image=self.logo_image, background="#1DA1F2")
        logo_label.pack(pady=10)

        # Title Label
        title_label = ttk.Label(self, text="Facebook Automation Tool", font=("Helvetica", 24, "bold"), background="#1DA1F2", foreground="white")
        title_label.pack(pady=10)

        # Notebook (Tab View)
        style = ttk.Style()
        # style.configure("TNotebook", background="#1DA1F2", foreground="white")
        # style.configure("TNotebook.Tab", background="white", foreground="black", padding=[5, 5])
        # style.map("TNotebook.Tab", background=[("selected", "black")], foreground=[("selected", "#1DA1F2")])

        style.theme_use("clam")
        style.configure("TButton", background="#4CAF50", foreground="white", font=('Arial', 10, 'bold'), padding=10)
        style.configure("TLabel", font=('Arial', 10), foreground="#333")
        style.configure("TEntry", font=('Arial', 10), padding=5)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(padx=10, pady=10, expand=True)

        # Tabs
        self.scrape_tab = ttk.Frame(self.notebook)
        self.post_action_tab = ttk.Frame(self.notebook)
        self.account_tab = ttk.Frame(self.notebook)
        self.post_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.scrape_tab, text="Scrape Users")
        self.notebook.add(self.post_action_tab, text="Post Actions")
        self.notebook.add(self.account_tab, text="Account Actions")
        self.notebook.add(self.post_tab, text="Post")

        # --- Tweet Link Tab UI ---
        self.create_scrape_tab()

        # --- Post Actions Tab UI ---
        self.create_post_actions_tab()

        # --- Account Tab UI ---
        self.create_account_tab()

        # --- Post Tweet Tab UI--
        self.create_post_tab()

    def create_scrape_tab(self):
        # Upload CSV button
        ttk.Button(self.scrape_tab, text="Upload CSV", command=self.load_csv).grid(row=0, column=0, padx=10, pady=10)
        self.csv_label_scrape = ttk.Label(self.scrape_tab, text="No file selected")
        self.csv_label_scrape.grid(row=0, column=1, padx=10, pady=10)
        self.csv_users = []

        ttk.Label(self.scrape_tab, text="Group/Post Link:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.link = ttk.Entry(self.scrape_tab, width=40)
        self.link.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.scrape_tab, text="File Name:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.file_name = ttk.Entry(self.scrape_tab, width=40)
        self.file_name.grid(row=2, column=1, padx=10, pady=10)

        # self.action_var = tk.StringVar(value="like")
        # actions = ["like", "like", "retweet", "report", "comment"]
        # self.action_dropdown = ttk.OptionMenu(self.scrape_tab, self.action_var, *actions, command=self.toggle_comment)
        # self.action_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # self.comment_label = ttk.Label(self.scrape_tab, text="Comment:")
        # self.comment_entry = ttk.Entry(self.scrape_tab, width=40)
        # self.paraphrase_var = tk.IntVar()
        # self.paraphrase_checkbox = ttk.Checkbutton(self.scrape_tab, text="Paraphrase", variable=self.paraphrase_var)
        # self.language_var = tk.StringVar(value="English")
        # self.language_dropdown = ttk.OptionMenu(self.scrape_tab, self.language_var, "English", "English", "Urdu", "Hindi", "Bengali")

        # ttk.Label(self.scrape_tab, text="Delay (seconds):").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        # self.delay_entry = ttk.Entry(self.scrape_tab, width=10)
        # self.delay_entry.grid(row=4, column=1, padx=10, pady=10)
        # self.delay_entry.insert(0, "1")

        ttk.Button(self.scrape_tab, text="Start", command=self.scrape_users).grid(row=5, column=1, padx=10, pady=10)

    def create_post_actions_tab(self):
        # Upload CSV button
        ttk.Button(self.post_action_tab, text="Upload CSV", command=self.load_csv).grid(row=0, column=0, padx=10, pady=10)
        self.csv_label_post_action = ttk.Label(self.post_action_tab, text="No file selected")
        self.csv_label_post_action.grid(row=0, column=1, padx=10, pady=10)
        self.csv_users = []

        ttk.Label(self.post_action_tab, text="Post Link:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.link_entry_post_action = ttk.Entry(self.post_action_tab, width=40)
        self.link_entry_post_action.grid(row=1, column=1, padx=10, pady=10)

        self.post_action_var = tk.StringVar(value="like")
        post_actions = ["like", "like", "comment"]
        self.post_action_dropdown = ttk.OptionMenu(self.post_action_tab, self.post_action_var, *post_actions, command=self.toggle_post_comment)
        self.post_action_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Comment feature in post tab
        self.post_action_comment_label = ttk.Label(self.post_action_tab, text="Comment:")
        self.post_action_comment_entry = ttk.Entry(self.post_action_tab, width=40)
        self.post_action_paraphrase_var = tk.IntVar()
        self.post_action_paraphrase_checkbox = ttk.Checkbutton(self.post_action_tab, text="Paraphrase", variable=self.post_action_paraphrase_var)
        self.post_action_language_var = tk.StringVar(value="English")
        self.post_action_language_dropdown = ttk.OptionMenu(self.post_action_tab, self.post_action_language_var, "English", "English", "Urdu", "Hindi", "Bengali")

        # ttk.Label(self.post_action_tab, text="Delay (seconds):").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        # self.post_delay_entry = ttk.Entry(self.post_action_tab, width=10)
        # self.post_delay_entry.grid(row=4, column=1, padx=10, pady=10)
        # self.post_delay_entry.insert(0, "1")

        ttk.Button(self.post_action_tab, text="Start", command=self.start_post_actions).grid(row=4, column=1, padx=10, pady=10)

    def create_account_tab(self):
        # Upload CSV button
        ttk.Button(self.account_tab, text="Upload CSV", command=self.load_csv).grid(row=0, column=0, padx=10, pady=10)
        self.csv_label_account = ttk.Label(self.account_tab, text="No file selected")
        self.csv_label_account.grid(row=0, column=1, padx=10, pady=10)
        self.csv_users = []

        ttk.Label(self.account_tab, text="Account Link:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.account_link = ttk.Entry(self.account_tab, width=40)
        self.account_link.grid(row=1, column=1, padx=10, pady=10)

        self.account_action_var = tk.StringVar(value="follow")
        account_actions = ["follow", "follow", "report", "message"]
        self.account_action_dropdown = ttk.OptionMenu(self.account_tab, self.account_action_var, *account_actions, command=self.toggle_message)
        self.account_action_dropdown.grid(row=2, column=1, padx=10, pady=10)

        self.message_label = ttk.Label(self.account_tab, text="Message:")
        self.message_entry = ttk.Entry(self.account_tab, width=40)
        self.account_paraphrase_var = tk.IntVar()
        self.account_paraphrase_checkbox = ttk.Checkbutton(self.account_tab, text="Paraphrase", variable=self.account_paraphrase_var)
        self.account_language_var = tk.StringVar(value="English")
        self.account_language_dropdown = ttk.OptionMenu(self.account_tab, self.account_language_var, "English", "English", "Urdu", "Hindi", "Bengali")

        ttk.Label(self.account_tab, text="Delay (seconds):").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.account_delay_entry = ttk.Entry(self.account_tab, width=10)
        self.account_delay_entry.grid(row=4, column=1, padx=10, pady=10)
        self.account_delay_entry.insert(0, "1")

        ttk.Button(self.account_tab, text="Start", command=self.start_account_actions).grid(row=5, column=1, padx=10, pady=10)

    def create_post_tab(self):
        # Upload CSV button
        ttk.Button(self.post_tab, text="Upload CSV", command=self.load_csv).grid(row=0, column=0, padx=10, pady=10)
        self.csv_label_post = ttk.Label(self.post_tab, text="No file selected")
        self.csv_label_post.grid(row=0, column=1, padx=10, pady=10)
        self.csv_users = []

        # ttk.Label(self.account_tab, text="Account Link:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        # self.account_link = ttk.Entry(self.account_tab, width=40)
        # self.account_link.grid(row=1, column=1, padx=10, pady=10)

        # self.account_action_var = tk.StringVar(value="follow")
        # account_actions = ["follow", "follow", "report", "message"]
        # self.account_action_dropdown = ttk.OptionMenu(self.account_tab, self.account_action_var, *account_actions, command=self.toggle_message)
        # self.account_action_dropdown.grid(row=2, column=1, padx=10, pady=10)

        self.post_message_label = ttk.Label(self.post_tab, text="Message:")
        self.post_message_entry = ttk.Entry(self.post_tab, width=40)
        self.post_paraphrase_var = tk.IntVar()
        self.post_paraphrase_checkbox = ttk.Checkbutton(self.post_tab, text="Paraphrase", variable=self.post_paraphrase_var)
        self.post_language_var = tk.StringVar(value="English")
        self.post_language_dropdown = ttk.OptionMenu(self.post_tab, self.post_language_var, "English", "English", "Urdu", "Hindi", "Bengali")
        self.post_message_label.grid(row=1, column=0, padx=10, pady=10)
        self.post_message_entry.grid(row=1, column=1, padx=10, pady=10)
        self.post_paraphrase_checkbox.grid(row=1, column=2, padx=10, pady=10)
        self.post_language_dropdown.grid(row=1, column=3, padx=10, pady=10)

        # Upload Images button
        ttk.Button(self.post_tab, text="Select Images Folder", command=self.load_image_folder).grid(row=2, column=0, padx=10, pady=10)
        self.image_label_post = ttk.Label(self.post_tab, text="No folder selected")
        self.image_label_post.grid(row=2, column=1, padx=10, pady=10)
        self.image_folder = ''
        tk.Button(self.post_tab, text="X", command=self.remove_image_folder).grid(row=2, column=2, padx=10, pady=10)


        # ttk.Label(self.post_tab, text="Delay (seconds):").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        # self.post_delay_entry = ttk.Entry(self.post_tab, width=10)
        # self.post_delay_entry.grid(row=3, column=1, padx=10, pady=10)
        # self.post_delay_entry.insert(0, "1")

        ttk.Button(self.post_tab, text="Start", command=self.start_posting).grid(row=3, column=1, padx=10, pady=10)

    def toggle_comment(self, *args):
        if self.action_var.get() == "comment":
            self.comment_label.grid(row=3, column=0, padx=10, pady=10)
            self.comment_entry.grid(row=3, column=1, padx=10, pady=10)
            self.paraphrase_checkbox.grid(row=3, column=2, padx=10, pady=10)
            self.language_dropdown.grid(row=3, column=3, padx=10, pady=10)
        else:
            self.comment_label.grid_forget()
            self.comment_entry.grid_forget()
            self.paraphrase_checkbox.grid_forget()
            self.language_dropdown.grid_forget()

    def toggle_post_comment(self, *args):
        if self.post_action_var.get() == "comment":
            self.post_action_comment_label.grid(row=3, column=0, padx=10, pady=10)
            self.post_action_comment_entry.grid(row=3, column=1, padx=10, pady=10)
            self.post_action_paraphrase_checkbox.grid(row=3, column=2, padx=10, pady=10)
            self.post_action_language_dropdown.grid(row=3, column=3, padx=10, pady=10)
        else:
            self.post_action_comment_label.grid_forget()
            self.post_action_comment_entry.grid_forget()
            self.post_action_paraphrase_checkbox.grid_forget()
            self.post_action_language_dropdown.grid_forget()

    def toggle_message(self, *args):
        if self.account_action_var.get() == "message":
            self.message_label.grid(row=3, column=0, padx=10, pady=10)
            self.message_entry.grid(row=3, column=1, padx=10, pady=10)
            self.account_paraphrase_checkbox.grid(row=3, column=2, padx=10, pady=10)
            self.account_language_dropdown.grid(row=3, column=3, padx=10, pady=10)
        else:
            self.message_label.grid_forget()
            self.message_entry.grid_forget()
            self.account_paraphrase_checkbox.grid_forget()
            self.account_language_dropdown.grid_forget()

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_users = load_csv_file(file_path)  # You can update this to actually load the CSV content.
            self.csv_label_post_action.config(text=file_path)  # Update label with the file path
            self.csv_label_post.config(text=file_path)  # Update label with the file path
            self.csv_label_account.config(text=file_path)  # Update label with the file path
            self.csv_label_scrape.config(text=file_path)  # Update label with the file path
        else:
            self.csv_label_scrape.config(text="No file selected")

    def load_image_folder(self):
        folder_path = filedialog.askdirectory()  # Ask the user to select a directory
        if folder_path:
            self.image_folder = folder_path
            self.image_label_post.config(text=folder_path)  # Update label with the file path
        else:
            self.image_label_post.config(text="No folder selected")

    def remove_image_folder(self):
        self.image_folder = ''
        self.image_label_post.config(text="No folder selected")

    def scrape_users(self):
        users = self.csv_users
        link = self.link.get()
        file_name = self.file_name.get()
        perform_action(link, users, action='scrape_users', filename=file_name)
            

    # def start_tweet_actions(self):
    #     tweet_link = self.tweet_link.get()
    #     action = self.action_var.get()
    #     comment = self.comment_entry.get() if action == "comment" else None
    #     paraphrase = bool(self.paraphrase_var.get())
    #     language = self.language_var.get()
    #     try:
    #         delay = int(self.delay_entry.get())
    #     except:
    #         messagebox.showerror('Error', 'Choose an integer for delay.')
    #         return
    #     users = self.csv_users
    #     perform_action(action, tweet_link=tweet_link, comment=comment, paraphrase=paraphrase, language=language, delay=delay, users=users, task_type='link')

    def start_post_actions(self):
        post = self.link_entry_post_action.get()
        action = self.post_action_var.get()
        comment = self.post_action_comment_entry.get() if action == "comment" else None
        paraphrase = bool(self.post_action_paraphrase_var.get())
        language = self.post_action_language_var.get()
        # try:
        #     delay = int(self.delay_entry.get())
        # except:
        #     messagebox.showerror('Error', 'Choose an integer for delay.')
        #     return
        users = self.csv_users
        perform_action(link=post, users=users, action=action, comment=comment, paraphrase=paraphrase, language=language)

    def start_account_actions(self):
        account_link = self.account_link.get()
        action = self.account_action_var.get()
        message = self.message_entry.get() if action == "message" else None
        paraphrase = bool(self.account_paraphrase_var.get())
        language = self.account_language_var.get()
        try:
            delay = int(self.delay_entry.get())
        except:
            messagebox.showerror('Error', 'Choose an integer for delay.')
            return
        users = self.csv_users
        perform_action(action, tweet_link=account_link, comment=message, paraphrase=paraphrase, language=language, delay=delay, users=users, task_type='account')

    def start_posting(self):
        message = self.post_message_entry.get()
        paraphrase = bool(self.post_paraphrase_var.get())
        language = self.post_language_var.get()
        image_folder = self.image_folder

        # try:
        #     delay = int(self.delay_entry.get())
        # except:
        #     messagebox.showerror('Error', 'Choose an integer for delay.')
        #     return
        users = self.csv_users
        perform_action(link=None, users=users, action='post', comment=message, paraphrase=paraphrase, language=language, image_folder=image_folder)


if __name__ == "__main__":
    app = XAutomationApp()
    app.mainloop()