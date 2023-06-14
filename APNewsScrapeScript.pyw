from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


ROOT_WIDTH = 800
ROOT_HEIGHT = 600


def get_firefox_webdriver():
    firefox_webdriver_options = FirefoxOptions()
    firefox_webdriver_options.add_argument("--headless")
    firefox_webdriver = webdriver.Firefox(firefox_webdriver_options)
    return firefox_webdriver

def get_unique_web_page_links(web_page_url:str, firefox_webdriver:webdriver.Firefox):
    firefox_webdriver.get(web_page_url)
    unique_web_page_links = []
    all_link_web_page_elements = firefox_webdriver.find_elements(By.XPATH, "//a[@href]")
    for link_web_page_element in all_link_web_page_elements:
        if link_web_page_element.get_attribute("href") not in unique_web_page_links:
            unique_web_page_links.append(link_web_page_element.get_attribute("href"))
    return unique_web_page_links

def get_strings_with_common_substring(substring:str, string_list:list[str],):
    strings_with_common_substring = []
    for string in string_list:
        if substring in string:
            strings_with_common_substring.append(string)
    return strings_with_common_substring

def get_apnews_web_page_article_headlines_and_links(hub_url:str, firefox_webdriver:webdriver.Firefox):
    firefox_webdriver.get(hub_url)
    article_headlines_and_links = []
    all_link_web_page_elements = firefox_webdriver.find_elements(By.XPATH, "//a[contains(@data-key,'card-headline')]")
    for link_web_page_element in all_link_web_page_elements:
        if "https://apnews.com/article/" in link_web_page_element.get_attribute("href"):
            article_headlines_and_links.append((link_web_page_element.text, link_web_page_element.get_attribute("href")))
    return article_headlines_and_links

def get_apnews_article_content(article_url:str, firefox_webdriver:webdriver.Firefox):
    firefox_webdriver.get(article_url)
    headline = firefox_webdriver.find_element(By.XPATH, "/html/body/div[2]/div/main/div[3]/div/div[4]/div[1]/h1").text
    author = firefox_webdriver.find_element(By.XPATH, "/html/body/div[2]/div/main/div[3]/div/div[4]/span/span[1]").text
    date = None
    try:
        date = firefox_webdriver.find_element(By.XPATH, "/html/body/div[2]/div/main/div[3]/div/div[4]/span/span[2]").get_attribute("title")
    except:
        pass
    story = firefox_webdriver.find_element(By.CLASS_NAME, "Article").text
    return (headline, author, date, story, article_url)


def make_scrollbar(frame:Tk):
    main_scrollbar_frame = Frame(frame)
    main_scrollbar_frame.pack(fill=BOTH, expand=1)

    scrollbar_canvas = Canvas(main_scrollbar_frame)
    scrollbar_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar = ttk.Scrollbar(main_scrollbar_frame, orient=VERTICAL, command=scrollbar_canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    scrollbar_canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar_canvas.bind('<Configure>', lambda e: scrollbar_canvas.configure(scrollregion=scrollbar_canvas.bbox("all")))

    outer_scrollbar_frame = Frame(scrollbar_canvas)

    scrollbar_canvas.create_window((0,0), window=outer_scrollbar_frame, anchor="nw")

    return outer_scrollbar_frame

def make_new_tab(tab_name:str, notebook:ttk.Notebook):
    new_tab = Frame(notebook, width=ROOT_WIDTH, height=ROOT_HEIGHT)
    new_tab.pack(fill="both", expand=1)
    notebook.add(new_tab, text=tab_name)
    return new_tab


def click_article_headline(article_headline_and_link:tuple, notebook:ttk.Notebook, firefox_webdriver:webdriver.Firefox):
    article_content = get_apnews_article_content(article_headline_and_link[1], firefox_webdriver)
    text = ""
    for item in article_content:
        if item != None:
            text += item + "\n\n"
    frame = make_new_tab(article_headline_and_link[0], notebook)
    Label(frame, text=text).grid(row=0, column=0)


root_apnews_window = Tk()
root_apnews_window.title("APNewsScrapeScript")
# root_apnews_window.iconbitmap()
root_apnews_window.geometry(f"{ROOT_WIDTH}x{ROOT_HEIGHT}")

second_apnews_frame = make_scrollbar(root_apnews_window)
tab_holder_notebook = ttk.Notebook(second_apnews_frame)
tab_holder_notebook.pack()
apnews_hub_tab = make_new_tab("AP Top News", tab_holder_notebook)

firefox_webdriver_apnews = get_firefox_webdriver()
url_top_apnews = "https://apnews.com/hub/ap-top-news"
links_top_apnews = get_unique_web_page_links(url_top_apnews, firefox_webdriver_apnews)

article_headlines_and_links = get_apnews_web_page_article_headlines_and_links(url_top_apnews, firefox_webdriver_apnews)

for i in range(len(article_headlines_and_links)):
    Button(
        apnews_hub_tab,
        text=article_headlines_and_links[i][0],
        command=lambda i=i: click_article_headline(article_headlines_and_links[i], tab_holder_notebook, firefox_webdriver_apnews)
    ).grid(
        row=i,
        column=0
    )
    

root_apnews_window.mainloop()

firefox_webdriver_apnews.quit()