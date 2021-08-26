from item_details import store_details
from items import get_category_names, get_subcategory_names, get_product_urls


def main():
    main_url = "https://webscraper.io"
    categories = get_category_names(main_url)

    for category in categories:
        subcategories = get_subcategory_names(main_url, category)
        for subcategory in subcategories:
            get_product_urls(main_url, category, subcategory)

    store_details()


if __name__ == '__main__':
    main()
