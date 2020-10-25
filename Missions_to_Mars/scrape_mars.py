import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time


def scrape(): 
    executable_path = {'executable_path': 'C:/Users/osafi/Desktop/BOOT CAMP/12 WEB SCRAPING/Web_Scrapping_Challenge_OS/Missions_to_Mars/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    time.sleep(5)
    soup = bs(html, 'html.parser')
    mars = soup.find('div', class_ = "list_text")
    news_title = mars.find('div', class_ = "content_title").text
    news_p = mars.find('div', class_ = "article_teaser_body").text
    mars_news = [news_title, news_p]

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    time.sleep(15)
    html = browser.html
    soup = bs(html, 'html.parser')
    browser.click_link_by_id("full_image")
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(15)
    more_info = soup.find('div', class_="addthis_toolbox addthis_default_style")['addthis:url']
    browser.click_link_by_partial_href(more_info)
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image = soup.find('img', class_="main_image")['src']
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(15)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_weather = results.find('span').text


    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(15)
    html = browser.html
    soup = bs(html, 'html.parser')
    facts = pd.read_html(facts_url)
    mars_facts = pd.DataFrame(facts[0])
    mars_facts_string = mars_facts.to_html(header = False, index = False)

    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    time.sleep(15)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_image_urls = []
    results = soup.find('div', class_ = 'result-list')
    hemi_pics = results.find_all('div', class_ = 'item')
    print(hemi_pics)
    for i in hemi_pics:
        title = i.find('h3').text
        title = title.replace("Enhanced", "")
        href = i.find('a')['href']
        image_url = "https://astrogeology.usgs.gov/" + href
        browser.visit(image_url)
        time.sleep(15)
        html = browser.html
        soup = bs(html, 'html.parser')
        full_size = soup.find('div', class_ = 'downloads')
        img_url = full_size.find('a')['href']
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})

    mars_data = {
        "mars_title": mars_news[0],
        "mars_news": mars_news[1],
        "featured_image": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts_string,
        "mars_hemis": hemisphere_image_urls
    }

    browser.quit()
    
    return(mars_data)  

# scrape()  # use for testing only




























