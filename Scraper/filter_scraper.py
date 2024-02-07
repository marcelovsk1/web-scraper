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
        {
            'name': 'Eventbrite',
            'url': 'https://www.eventbrite.com/d/canada--montreal/events/',
            'selectors': {
                'event': {'tag': 'div', 'class': 'Stack_root__1ksk7'},
                'Event': {'tag': 'h2', 'class': 'Typography_root__487rx #3a3247 Typography_body-lg__487rx event-card__clamp-line--two Typography_align-match-parent__487rx'},
                'Date': {'tag': 'p', 'class': 'Typography_root__487rx #3a3247 Typography_body-md-bold__487rx Typography_align-match-parent__487rx'},
                'Location': {'tag': 'p', 'class': 'Typography_root__487rx #585163 Typography_body-md__487rx event-card__clamp-line--one Typography_align-match-parent__487rx'},
                'Image URL': {'tag': 'img', 'class': 'event-card-image'}
            }
        }
    ]

    all_events = []

    for source in sources:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        events = scrape_events(driver, source['url'], source['selectors'])
        driver.quit()

        source_data = {
            'source_name': source['name'],
            'events': events
        }

        all_events.append(source_data)

    # FILTER
    filtered_events = []
    seen_events = set()

    # === DE-DUPLICATE EVENTS ===
    # 1. similarity test of event names --> find a library that calculates a similarity score bewteen strings
    # for example: "New Year Party" = "NY Party"
    # 2. if we have troubles with this way, we could do embeddings but that is slighty more difficult to implement

    # === FORMAT ELEMENTS (we have to check how is this formatted in the database) ===
    # 1. Date -> Python datetime Object
        # if events from the same website have their date formatted the same way, then you could make a special formatting function
        # for each website
        # Ticketmaster: "Fri 3, October" => function to output day, month, year =>> ({ day: 3, month: 10, year: null }) // 2024
        # you can use those elements to create a new datetime object in python which will be use to save the date in the database in the same way as the other dates

    # 2. Location
        # a. If it's stored as simple string, then we could be fine
            # maybe we still need to do some cleaning to format location the same way (Montreal <> Montréal)
        # b. If we need coordinates, or more information on the location, or to format it the same way
            # I would use Google Places API which take as input an unformated dalocationte and returns a formatted place
            # it has a cost but it's usefull (like Google Maps)

    # 3. Image URL
        # => no special need but depending on the current way of saving image
        # we would need to save the image in our own servers like the other images

# make a list of duplicate events to compare

# scrape secondary pages

# gpt prompt for generating tags from title and description


    # star
    for source_data in all_events:
        source_name = source_data['source_name']
        events = source_data['events']

        for event in events:
            event_key = (event['Event'], event['Date'], event['Location'], event['Image URL'])
            if event_key not in seen_events:
                seen_events.add(event_key)
                filtered_events.append({
                    'source_name': source_name,
                    'event_name': event['Event'],
                    'date': event['Date'],
                    'location': event['Location'],
                    'image_url': event['Image URL']
                })

    file_name = "events_data1.json"
    with open(file_name, "w") as json_file:
        json.dump(filtered_events, json_file, indent=2)

    print(f"JSON data has been written to {file_name}")

if __name__ == "__main__":
    main()
