from bs4 import BeautifulSoup
import requests
import csv
import json
import pandas as pd

# List of item names to search on eBay
input_name = "iphone"

# Returns a list of urls that search eBay for an item
def make_urls(names):

    # eBay url that can be modified to search for a specific item on eBay
    serach_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw="
    # Replace spaces in request from form with +
    url = serach_url + names.replace(" ", "+")
    # Returns completed url
    return url

# Scrapes and prints the url, name, and price of the first item result listed on eBay
def scrape(url):
        # Downloads the eBay page for processing
        res = requests.get(url)
        # Raises an exception error if there's an error downloading the website
        res.raise_for_status()
        # Creates a BeautifulSoup object for HTML parsing
        soup = BeautifulSoup(res.text, 'html.parser')
        item_wrapper = soup.find_all(attrs={'class':'s-item__wrapper clearfix'})

        item_data = []

        # looping for make a list of dictionary items as item data
        # persiapan data untuk membuat csv, xlsx, dan json file
        for items in item_wrapper:
            # get product's url
            product_link = items.find("a",{"class": "s-item__link"})['href']
            # get product's image url
            image_link = items.find("img",{"class": "s-item__image-img"})['src']
            # get product's name
            name = items.find("h3", {"class": "s-item__title"}).get_text(separator=u" ")
            # get product's price
            price = items.find("span", {"class": "s-item__price"}).get_text()

            # Prints listed item name, and the price of the item
            # print("Item Link: " + product_link)
            # print("Item Name: " + name)
            # print("Price: " + price)
            # print("Image Link: " + image_link + "\n")

            # make a list of dictionary's item
            item_data.append(
                dict(image_link=image_link,name=name,price=price,product_link=product_link)
            )

        if len(item_data) != 0:
            # save as csv using csv package
            keys = item_data[0].keys()
            with open('project/files/ebays_product.csv', 'w') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(item_data)

            # save as json using json package
            to_json = dict(data=item_data)
            with open('project/files/ebays_product.json', 'w') as outfile:
                json.dump(to_json, outfile)

            # save as excel xlsx, csv dan json using pandas package
            df = pd.DataFrame.from_dict(item_data)
            print(df)
            df.to_excel('project/files/ebays_product.xlsx')
            # df.to_csv('ebays_product.csv')
            # df.to_json('ebays_product.json')

        # return final item
        return item_data

        # print(item_data)

# Runs the code for training the function above before useing flask
# scrape(make_urls(input_name))
# print(make_urls(input_name))