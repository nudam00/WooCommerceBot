from re import A
from bot import Bot
from multiprocessing import Pool
from scraping import Scraping
from datetime import datetime
import xlrd

ip = ""  # paste your ip


def createTasks(number):
    threads = []
    wb = xlrd.open_workbook("login.xlsx")
    sheet = wb.sheet_by_index(0)
    for i in range(number):
        username = sheet.cell_value(i, 0)
        password = sheet.cell_value(i, 1)
        email = sheet.cell_value(i, 2)
        threads.append(
            Bot(
                ip,
                "http://{}/wordpress/produkt/boncellensis-secullant/".format(
                    ip),
                username,
                password,
                email,
            )
        )
    return threads


def a(bot):
    bot.purchase(account=False, registration=False)


def b(bot):
    bot.purchase(account=True, registration=False)


def c(bot):
    bot.purchase(account=False, registration=True)


def d(bot):
    bot.purchase(account=True, registration=True)


def e(bot):
    bot.purchase(checkout=True, registration=True)


def aa(bot):
    bot.purchase(account=False, registration=False, captcha=True)


def bb(bot):
    bot.purchase(account=True, registration=False, captcha=True)


def cc(bot):
    bot.purchase(account=False, registration=True, captcha=True)


def dd(bot):
    bot.purchase(account=True, registration=True, captcha=True)


def ee(bot):
    bot.purchase(checkout=True, registration=True, captcha=True)


def runThreads(k):
    numberTasks = 35  # number of tasks
    tasks = createTasks(numberTasks)
    p = Pool(numberTasks)
    if k == "1":
        p.map(a, tasks)
    if k == "2":
        p.map(b, tasks)
    if k == "3":
        p.map(c, tasks)
    if k == "4":
        p.map(d, tasks)
    if k == "5":
        p.map(e, tasks)
    if k == "6":
        p.map(aa, tasks)
    if k == "7":
        p.map(bb, tasks)
    if k == "8":
        p.map(cc, tasks)
    if k == "9":
        p.map(dd, tasks)
    if k == "10":
        p.map(ee, tasks)


def runScraping(categoryLink):
    scraper = Scraping(categoryLink)
    scraper.writeExcel()


def choice(i, k):
    if i == "1":
        runThreads(k)
    if i == "2":
        runScraping("http://{}/wordpress/kategoria-produktu/plants/".format(ip))


if __name__ == "__main__":
    print("1. Bot\n" "2. Scraping\n")
    i = input()
    if i == "1":
        print(
            "1. Bot without account\n"
            "2. Logging in before checkout\n"
            "3. Registration\n"
            "4. Logging into My Account\n"
            "5. Register while checkout\n"
            "6. Bot without account (with CAPTCHA)\n"
            "7. Logging in before checkout (with CAPTCHA)\n"
            "8. Registration (with CAPTCHA)\n"
            "9. Logging into My Account (with CAPTCHA)\n"
            "10. Register while checkout (with CAPTCHA)"
        )
        k = input()
    else:
        k = None
    first_time = datetime.now()
    choice(i, k)
    later_time = datetime.now()
    difference = later_time - first_time
    print(difference)
