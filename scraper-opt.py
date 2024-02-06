import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Function to scroll to bottom
def scroll_to_bottom(driver, max_clicks=3):
    for _ in range(max_clicks):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

# Events to scrape
def scrape_events(driver, url, selectors):
    driver.get(url)
    driver.implicitly_wait(30)
    scroll_to_bottom(driver)

    page_content = driver.page_source
    webpage = BeautifulSoup(page_content, 'html.parser')

    events = webpage.find_all(selectors['event']['tag'], class_=selectors['event'].get('class'))
    event_list = []

    for event in events:
        event_info = {}
        for key, selector in selectors.items():
            if key != 'event':
                element = event.find(selector['tag'], class_=selector.get('class'))
                event_info[key] = element.text.strip() if element else None
                if key == 'Image URL':
                    event_info[key] = element['src'] if element and 'src' in element.attrs else None

        event_list.append(event_info)

    return event_list

def main():
    sources = [
        {
            'name': 'Facebook',
            "loadingTime": 10,
            'url': 'https://www.facebook.com/events/explore/montreal-quebec/102184499823699/',
            'selectors': {
                'event': {'tag': 'div', 'class': 'x78zum5 x1n2onr6 xh8yej3'},
                'Event': {'tag': 'span', 'class': 'x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j'},
                'Date': {'tag': 'div', 'class': 'xu06os2 x1ok221b'},
                'Location': {'tag': 'span', 'class': 'x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j'},
                'Image URL': {'tag': 'img', 'class': 'x1rg5ohu x5yr21d xl1xv1r xh8yej3'}
            }
        },
        {
            'name': 'Ticketmaster',
            'url': 'https://www.ticketmaster.ca/discover/concerts/montreal',
            'selectors': {
                'event': {'tag': 'div', 'class': 'Flex-sc-145abwg-0 bWTqsV accordion__item event-listing__item'},
                'Event': {'tag': 'div', 'class': 'sc-fFeiMQ bCvzDL text text--dark text--primary sc-6jnhqk-0 kGOLzf event-tile__title'},
                'Date': {'tag': 'div', 'class': 'sc-fFeiMQ dBYlim text text--accent text--accent01 text-tm sc-17ev1tv-0 cnj20n-0 firocR iZsGLV event-tile__date-title'},
                'Location': {'tag': 'div', 'class': 'sc-fFeiMQ iIgzpz text text--dark text--secondary sc-1s3i3gy-0 hbRPym event-tile__sub-title'},
                'Image URL': {'tag': 'img', 'class': 'event-listing__thumbnail'}
            }
        },
