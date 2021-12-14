#imports
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
#import requests
#import pymongo
import datetime as dt



#scrape all function
def scrape_all():
    print("Scrape all was successful")
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser= Browser('chrome', **executable_path, headless=False)





    news_title, news_para = scrape_news(browser)

    marsData = {
        "newsTitle" : news_title,
        "newsParagraph" : news_para,
        "featuredImage" : scrape_feature_image(browser),
        "factsTable" : scrape_facts(browser),
        "hemispheres" : scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }

    browser.quit()

    return marsData

#scrape mars news
def scrape_news(browser):
    url = "https://redplanetscience.com/"
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    sld_element = news_soup.select_one('div.list_text')
    news_title = sld_element.find('div', class_='content_title')
    news_title = news_title.get_text()
    news_para = sld_element.find('div', class_='article_teaser_body')
    news_para = news_para.get_text()
    #return
    return news_title, news_para 
#scrape featured image page
def scrape_feature_image(browser):
    url='https://spaceimages-mars.com/'
    browser.visit(url)
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    img_rel = img_soup.find('img', class_='fancybox-image').get('src')
    img_fullurl= f'https://spaceimages-mars.com/{img_rel}'

    return img_fullurl

#scrape through facts page
def scrape_facts(browser):
    url='https://galaxyfacts-mars.com/'
    browser.visit(url)
    html = browser.html
    fact_soup = BeautifulSoup(html, 'html.parser')

    facts_location = (fact_soup.find('div', class_='diagram mt-4'))
    fact_table = (facts_location.find('table'))

    facts =""
    facts += str(fact_table)

    return facts
#scrape through hemispheres
def scrape_hemispheres(browser):
    url = "https://marshemispheres.com/"
    browser.visit(url)
    hemisphere_img_urls = []
    for i in range(4):
        hemisphereImg = {}
    
        browser.find_by_css('a.product-item img')[i].click()
        sample = browser.links.find_by_text('Sample').first
        hemisphereImg['url'] = sample['href']
    
        hemisphere_img_urls.append(hemisphereImg)
    #Get titles
        hemisphereImg['title'] = browser.find_by_css('h2.title').text
    
        browser.back()

    return hemisphere_img_urls
#setup flask app
if __name__ == "__main__":
    print(scrape_all())