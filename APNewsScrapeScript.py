from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def get_firefox_webdriver():
    firefox_webdriver_options = FirefoxOptions()
    firefox_webdriver_options.add_argument("--headless")
    firefox_webdriver = webdriver.Firefox(options=firefox_webdriver_options)
    return firefox_webdriver


def get_unique_web_page_links(web_page_url:str):
    firefox_webdriver = get_firefox_webdriver()
    firefox_webdriver.get(web_page_url)
    unique_web_page_links = []
    all_links_on_web_page = firefox_webdriver.find_elements(By.XPATH, "//a[@href]")
    for link_on_web_page in all_links_on_web_page:
        if link_on_web_page.get_attribute("href") not in unique_web_page_links:
            unique_web_page_links.append(link_on_web_page.get_attribute("href"))
    firefox_webdriver.quit()
    return unique_web_page_links


def get_strings_with_common_substring(list:list[str], substring:str):
    strings_with_common_substring = []
    for string in list:
        if substring in string:
            strings_with_common_substring.append(string)
    return strings_with_common_substring


apnews_web_page_url = "https://apnews.com/"
unique_apnews_web_page_links = get_unique_web_page_links(apnews_web_page_url)
apnews_hub_web_page_urls = get_strings_with_common_substring(unique_apnews_web_page_links, "https://apnews.com/hub/")


boowomp = []

for apnews_hub_web_page_url in apnews_hub_web_page_urls:
    apnews_hub_web_page_links = get_unique_web_page_links(apnews_hub_web_page_url)
    apnews_hub_article_web_page_links = get_strings_with_common_substring(apnews_hub_web_page_links, "https://apnews.com/article/")
    boowomp.append(apnews_hub_article_web_page_links)

print(boowomp)
# Article