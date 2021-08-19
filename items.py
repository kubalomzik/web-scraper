import csv

import bs4
import requests
from tqdm import tqdm


def get_category_names(main_url):
    response = requests.get("%s/test-sites/e-commerce/static" % main_url).text
    soup = bs4.BeautifulSoup(response, 'html.parser')

    categories_raw = soup.find_all("a", class_="category-link")
    categories = list()

    for category in categories_raw:
        categories.append(category.text.strip().lower())

    return categories


def get_subcategory_names(main_url, category):
    response = requests.get("%s/test-sites/e-commerce/static/%s" % (main_url, category)).text
    soup = bs4.BeautifulSoup(response, 'html.parser')

    subcategories_raw = soup.find_all("a", class_="subcategory-link")
    subcategories = list()

    for subcategory in subcategories_raw:
        subcategories.append(subcategory.text.strip().lower())

    return subcategories


def get_product_urls(main_url, category, subcategory):
    response = requests.get("%s/test-sites/e-commerce/static/%s/%s" % (main_url, category, subcategory)).text
    soup = bs4.BeautifulSoup(response, 'html.parser')

    next_page_sign = soup.find("a", rel="next")
    last_page = int(next_page_sign.find_previous("a", class_="page-link").text)

    for each_page in tqdm(range(1, last_page + 1)):

        response = requests.get("%s/test-sites/e-commerce/static/%s/%s?page=%i"
                                % (main_url, category, subcategory, each_page)).text
        soup = bs4.BeautifulSoup(response, 'html.parser')

        all_urls = soup.find_all(class_="title")
        all_href = list()

        for url in all_urls:
            all_href.append(main_url + url['href'])

        with open('all_items.csv', 'a') as csv_w:
            csv_writer = csv.writer(csv_w, delimiter=',', lineterminator='\n')
            with open('all_items.csv') as csv_r:
                csv_reader = csv.reader(csv_r)
                flag = 0
                for href in all_href:
                    for line in csv_reader:
                        if href in line:
                            flag = 1
                    if flag == 0:
                        csv_writer.writerow([href])
