from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def get_firefox_webdriver():
    firefox_webdriver_options = FirefoxOptions()
    firefox_webdriver_options.add_argument("--headless")
    firefox_webdriver = webdriver.Firefox(firefox_webdriver_options)
    return firefox_webdriver


def get_unique_web_page_links(web_page_url:str, firefox_webdriver:webdriver.Firefox):
    unique_web_page_links = []
    firefox_webdriver.get(web_page_url)
    all_web_page_links = firefox_webdriver.find_elements(By.XPATH, "//a[@href]")
    for web_page_link in all_web_page_links:
        if web_page_link.get_attribute("href") not in unique_web_page_links:
            unique_web_page_links.append(web_page_link.get_attribute("href"))
    return unique_web_page_links


def get_strings_with_common_substring(substring:str, string_list:list[str],):
    strings_with_common_substring = []
    for string in string_list:
        if substring in string:
            strings_with_common_substring.append(string)
    return strings_with_common_substring


def get_apnews_article_content(article_url:str, firefox_webdriver:webdriver.Firefox):
    firefox_webdriver.get(article_url)
    title = firefox_webdriver.find_element(By.XPATH, "/html/body/div[2]/div/main/div[3]/div/div[4]/div[1]/h1").text
    author = firefox_webdriver.find_element(By.XPATH, "/html/body/div[2]/div/main/div[3]/div/div[4]/span/span[1]").text
    date = firefox_webdriver.find_element(By.XPATH, "/html/body/div[2]/div/main/div[3]/div/div[4]/span/span[2]").get_attribute("title")
    story = firefox_webdriver.find_element(By.CLASS_NAME, "Article").text
    return (title, author, date, story)


firefox_apnews_webdriver = get_firefox_webdriver()
ap_top_news_url = "https://apnews.com/hub/ap-top-news"
ap_top_news_links = get_unique_web_page_links(ap_top_news_url, firefox_apnews_webdriver)
ap_top_news_article_urls = get_strings_with_common_substring("https://apnews.com/article/", ap_top_news_links)

for ap_top_news_article_url in ap_top_news_article_urls:
    print(get_apnews_article_content(ap_top_news_article_url, firefox_apnews_webdriver))

firefox_apnews_webdriver.quit()