import csv
import re
import time

import bs4
import requests
from tqdm import tqdm


def _scrape_details(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    details_raw = soup.find("div", class_="col-lg-10")

    hdd_sizes_raw = soup.find_all(class_=re.compile(".*btn swatch.*"), disabled=False)
    hdd_sizes_list = list()

    for hdd_size in hdd_sizes_raw:
        hdd_sizes_list.append(hdd_size.text.strip())

    hdd_sizes = ", ".join(hdd_sizes_list)

    return {
        "url": url,
        "name": details_raw.select("h4")[1].text,
        "price": details_raw.h4.text,
        "description": details_raw.p.text,
        "hdd_sizes": hdd_sizes,
        "reviews": details_raw.find(class_="ratings").text.strip(),
        "id": url.split('/')[-1],
        "scraping_date": str(time.strftime("%Y-%m-%d %H:%M"))
    }


def store_details():
    with open('all_items.csv') as csv_r, open('all_item_details.csv', 'a') as csv_w:

        csv_writer = csv.DictWriter(csv_w, fieldnames=["url", "type", "name", "price", "description", "hdd_sizes",
                                                       "reviews", "id", "scraping_date"])
        csv_writer.writeheader()
        csv_reader = csv.reader(csv_r)

        for line in tqdm(csv_reader):
            try:
                url = line[0]
                response = _scrape_details(url)
                csv_writer.writerow(response)
            except Exception as e:
                print(e)
