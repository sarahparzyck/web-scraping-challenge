from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import pandas as pd
from selenium import webdriver

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=True)

def scrape():
    browser = init_browser()

    #NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('li', class_='slide').find('div', class_='content_title').text
    news_paragraph = soup.find('div', class_='article_teaser_body').text

    #JPL Mars Space Images - Featured Image
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)

    fi_button = browser.click_link_by_id('full_image')
    time.sleep(15)

    browser.is_element_present_by_text("more info", wait_time=2)
    mi_button = browser.links.find_by_partial_text("more info")
    mi_button.click()
    time.sleep(15)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    srcs = [img['src'] for img in soup.find_all('img')]
    featured_image_url = f"https://www.jpl.nasa.gov{srcs[6]}"

    #Mars Facts
    url_4 = 'https://space-facts.com/mars/'
    browser.visit(url_4)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    facts_table = soup.find('table', attrs={"id": "tablepress-p-mars-no-2"})

    table_rows = facts_table.find_all('tr')
    table_elements = facts_table.find_all('td')
    row_values = []

    for rows in table_rows:
        data = rows.find_all('td') 
        values = [rows.text.strip() for rows in data if rows.text.strip()]
        if values:
            row_values.append(values)

    column_names = ['Description', 'value']
    mars_weather_df = pd.DataFrame(row_values, columns=column_names)

    html_table = mars_weather_df.to_html()

    mars_table = html_table.replace('\n', '')

    #Mars Hemispheres
    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    images = soup.find_all('div', class_='item')

    for image in images:
        title = image.find('h3').text
        link = image.img['src']

        hemisphere_image_urls = {
            'title': title,
            'img_url': f'https://astrogeology.usgs.gov/{link}',
        }

    #Store data in a dictionary
    mars_data = {
        "news_title" : news_title,
        "news_paragraph" : news_paragraph,
        "featured_image_url" : featured_image_url,
        "mars_table" : mars_table,
        "hemisphere_image_urls" : hemisphere_image_urls
    }

    browser.quit()

    return mars_data