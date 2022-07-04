import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime


class Bot:
    def __init__(self, ip, product_link, username, password, email):
        self.product_link = product_link
        self.s = requests.Session()
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Length": "441",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://{}/wordpress".format(ip),
            "Referer": "http://{}/wordpress/checkout/".format(ip),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.username = username
        self.password = password
        self.sitekey = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
        self.captchaapi = "c85f8ddb51d6df65e9ec5fde324a0f9f"
        self.ip = ip
        self.email = email

    def addToCart(self):
        response = requests.get(self.product_link).text
        soup = BeautifulSoup(response, "lxml")
        value = soup.find("button", {"name": "add-to-cart"}).get("value")
        response = self.s.get(
            "http://{}/wordpress/checkout/?add-to-cart={}".format(
                self.ip, value)
        ).text
        return response

    def getCheckoutNonce(self, response):
        soup = BeautifulSoup(response, "lxml")
        nonce = soup.find("input", {"id": "woocommerce-process-checkout-nonce"}).get(
            "value"
        )
        return nonce

    def getRegisterNonce(self):
        response = self.s.get(
            "http://{}/wordpress/my-account/".format(self.ip)).text
        soup = BeautifulSoup(response, "lxml")
        nonce = soup.find(
            "input", {"id": "woocommerce-register-nonce"}).get("value")
        return nonce

    def register(self, captchaURL=None):
        nonce = self.getRegisterNonce()
        data = {
            "username": "hghgfe",
            "email": "nbvnbv@gmail.com",
            "password": "dyplom22!",
            "woocommerce-register-nonce": nonce,
            "_wp_http_referer": "/wordpress/my-account/",
            "register": "Zarejestruj się",
        }

        if captchaURL != None:
            token = self.getCaptcha(captchaURL)
            data["g-recaptcha-response"] = token
        response = self.s.post(
            url="http://{}/wordpress/my-account/".format(self.ip),
            data=data,
            headers=self.headers,
        ).text
        soup = BeautifulSoup(response, "lxml")
        if "Kokpit" in str(soup):
            print("Successful registration")

    def getLoginNonce(self, url):
        response = self.s.get(url).text
        soup = BeautifulSoup(response, "lxml")
        nonce = soup.find(
            "input", {"id": "woocommerce-login-nonce"}).get("value")
        return nonce

    def loginAccount(self, captchaURL=None):
        nonce = self.getLoginNonce(
            "http://{}/wordpress/my-account/".format(self.ip))
        data = {
            "username": self.username,
            "password": self.password,
            "woocommerce-login-nonce": nonce,
            "_wp_http_referer": "/wordpress/my-account/",
            "login": "Zaloguj się",
        }
        if captchaURL != None:
            token = self.getCaptcha(captchaURL)
            data["g-recaptcha-response"] = token
        response = self.s.post(
            url="http://{}/wordpress/my-account/".format(self.ip),
            data=data,
            headers=self.headers,
        ).text
        soup = BeautifulSoup(response, "lxml")
        if "Kokpit" in str(soup):
            print("Successful login")

    def loginCheckout(self, captchaURL=None):
        nonce = self.getLoginNonce(
            "http://{}/wordpress/checkout/".format(self.ip))
        data = {
            "username": self.username,
            "password": self.password,
            "woocommerce-login-nonce": nonce,
            "_wp_http_referer": "/wordpress/checkout/",
            "redirect": "http://{}/wordpress/checkout/".format(self.ip),
            "login": "Logowanie",
        }
        if captchaURL != None:
            token = self.getCaptcha(captchaURL)
            data["g-recaptcha-response"] = token

        response = self.s.post(
            url="http://{}/wordpress/checkout/".format(self.ip),
            data=data,
            headers=self.headers,
        ).text
        soup = BeautifulSoup(response, "lxml")
        if "Dane płatności" in str(soup):
            print("Successful login")
        return response

    def getCaptcha(self, url):
        print("Getting Captcha from 2Captcha")
        first_time = datetime.now()
        s = requests.Session()

        captcha_id = s.post(
            "http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(
                self.captchaapi,
                self.sitekey,
                url,
            )
        ).text.split("|")[1]
        recaptcha_answer = s.get(
            "http://2captcha.com/res.php?key={}&action=get&id={}".format(
                self.captchaapi, captcha_id
            )
        ).text
        print("Solving Captcha...")
        while "CAPCHA_NOT_READY" in recaptcha_answer:
            time.sleep(1)
            recaptcha_answer = s.get(
                "http://2captcha.com/res.php?key={}&action=get&id={}".format(
                    self.captchaapi, captcha_id
                )
            ).text
        recaptcha_answer = recaptcha_answer.split("|")[1]
        later_time = datetime.now()
        difference = later_time - first_time
        return recaptcha_answer

    def purchase(self, account=None, registration=None, checkout=None, captcha=None):

        data = {
            "wc-ajax": "checkout",
            "billing_first_name": "aa",
            "billing_last_name": "aa",
            "billing_company": "",
            "billing_country": "PL",
            "billing_address_1": "aa 3",
            "billing_address_2": "",
            "billing_postcode": "62-050",
            "billing_city": "Mosina",
            "billing_state": "",
            "billing_phone": "125845956",
            "billing_email": self.email,
            "order_comments": "",
            "payment_method": "cod",
            "_wp_http_referer": "/wordpress/?wc-ajax=update_order_review",
        }

        # Five options (+5 with captcha):
        # 1. Buying without an account
        if account == False and registration == False:
            response = self.addToCart()
        # 2. Logging in before placing an order
        if account == True and registration == False:
            self.addToCart()
            if captcha == True:
                response = self.loginCheckout(
                    "http://{}/wordpress/checkout/".format(self.ip)
                )
            else:
                response = self.loginCheckout()
        # 3. Registration (change data each time)
        if account == False and registration == True:
            if captcha == True:
                self.register(
                    "http://{}/wordpress/my-account/".format(self.ip))
                response = self.addToCart()
            else:
                self.register()
                response = self.addToCart()
        # 4. First logging in, then placing an order
        if account == True and registration == True:
            if captcha == True:
                self.loginAccount(
                    "http://{}/wordpress/my-account/".format(self.ip))
                response = self.addToCart()
            else:
                self.loginAccount()
                response = self.addToCart()
        # 5. Registration when placing an order
        if checkout == True and registration == True:
            response = self.addToCart()
            data["account_username"] = self.username
            data["account_password"] = self.password

        nonce = self.getCheckoutNonce(response)
        data["woocommerce-process-checkout-nonce"] = nonce

        token = self.getCaptcha(
            "http://{}/wordpress/checkout/".format(self.ip))
        data["g-recaptcha-response"] = token

        response = self.s.post(
            url="http://{}/wordpress/?wc-ajax=checkout".format(self.ip),
            data=data,
            headers=self.headers,
        ).text
        soup = BeautifulSoup(response, "lxml")
        if "success" in str(soup):
            print("Successful checkout")
