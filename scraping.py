import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from openpyxl import Workbook


# Scraps item names with prices
class Scraping:
    def __init__(self, product_link):
        self.product_link = product_link

    def scrapeName(self):
        response = requests.get(self.product_link).text
        soup = BeautifulSoup(response, "lxml")
        h2 = soup.find_all("h2", {"class": "woocommerce-loop-product__title"})
        names = []
        for i in range(len(h2)):
            names.append(h2[i].getText())
        return names

    def scrapePrice(self):
        response = requests.get(self.product_link).text
        soup = BeautifulSoup(response, "lxml")
        span = soup.find_all(
            "span", {"class": "woocommerce-Price-amount amount"})
        prices = []
        for i in range(len(span)):
            prices.append(span[i].getText())
        return prices

    def excelFile(self):
        try:
            os.remove("products.xlsx")
        except FileNotFoundError:
            pass
        wb = Workbook()
        wb.save(filename="products.xlsx")

    def writeExcel(self):
        self.excelFile()

        names = self.scrapeName()
        prices = self.scrapePrice()
        df = pd.DataFrame(columns=["Name", "Price"])
        for i in range(len(names)):
            row = {"Name": names[i], "Price": prices[i]}
            df = df.append(row, ignore_index=True)
        with pd.ExcelWriter("products.xlsx", engine="openpyxl", mode="a") as writer:
            df.to_excel(writer, sheet_name="products")
        writer.save()
        writer.close()
        print("Successful scraping")
