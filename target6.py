import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime

used_list = []
used_count = 0


def used_counter():
        global used_count
        if used_count > 9:
                global used_list
                used_list = []
                used_count = 0
        used_count += 1

def error_hook(error):
	url = 'https://discordapp.com/api/webhooks/707320496399843399/p3xqylkmJY4T3U6MxgxTnQx6y297e8fH5rfIaIaBk9wsio8PJd7jKYX8FLBZM1Ak1o6N'
	requests.post(url, data=json.dumps({'username': 'Target Monitor', 'content': '{} <@&699658510786494546>'.format(error)}), headers={"Content-Type": "application/json"})

def webhook(name, address, pid, qty):
        blacklist = ['SD 5', 'MN 5', 'WI 5', 'AL 3']
        product_link = ("https://www.target.com/p/-/A-{}".format(pid))
        url = "https://discordapp.com/api/webhooks/706970539071242292/6gH5YHCF3UNDz8fwoe2gsiE-7qhG3nNVBpnpiMVTIqttnUUwRdQXtr4F2ej7He3VfO84"
        page = requests.get(product_link)

        soup = BeautifulSoup(page.text, 'html.parser')
        title = soup.find('title').text
        images = soup.find_all('img')
        image_url = (images[0]['src'])


        data = {}
        data["username"] = "Target Monitor"

        data["embeds"] = []
        embed = {}
        embed["title"] = title
        embed["color"] = 0xff0000
        embed["thumbnail"] = {"url" : image_url}
        embed["footer"] = {"text" : datetime.now().strftime('%m-%d-%Y %H:%M:%S')}
        embed["description"] = ("**Store Name:** {}\n**Store Address:** {}\n**Quantity Available:** {}\n{}".format(name, address, qty, product_link))
        data["embeds"].append(embed)

        global used_list
        if not any(s in name for s in used_list):
                if not any(s in address for s in blacklist):
                        #result2 = requests.post('https://discordapp.com/api/webhooks/706970539071242292/6gH5YHCF3UNDz8fwoe2gsiE-7qhG3nNVBpnpiMVTIqttnUUwRdQXtr4F2ej7He3VfO84', data=json.dumps(data), headers={"Content-Type": "application/json"})
                        result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})

                        try:
                            result.raise_for_status()
                        except requests.exceptions.HTTPError as err:
                            print(err)
                        else:
                            print("Webhook successfully sent, code {}.".format(result.status_code))


def monitor(products):
	product_ids = products
	for product in product_ids:
		try:
			monitor = requests.get('https://api.target.com/fulfillment_aggregator/v1/fiats/{}?key=eb2551e4accc14f38cc42d32fbc2b2ea&nearby=94404&limit=20&requested_quantity=1&radius=5000&include_only_available_stores=true&fulfillment_test_mode=grocery_opu_team_member_test'.format(product))
			res = monitor.json()

			locations = res['products'][0]['locations']
			for location in locations:
				name = location['store_name']
				address = location['store_address']
				qty_avail = location['location_available_to_promise_quantity']
				print("[{}]".format(product), end=" ")
				if location['order_pickup']['availability_status'] == "IN_STOCK":
					print("%-30s: IN STOCK for Store Pickup" % (name))
					global used_list
					webhook(name, address, product, int(qty_avail))
					used_list.append(name)
				else:
					print("%-30s: UNAVAILABLE" % (name))
		except Exception as g:
			print(g)
			error_hook(g)

if __name__ == '__main__':
	product_ids = ['77428671', '77428670', '16747574', '79366634', '79366642', '79503655']	#	Neon: 77464001, Grey: 77464002

	print(" Target In-Store Monitor")
	print(" Created by enrique#2519")
	print("**************************\n")
	print("Products Loaded: ")
	for i in range(len(product_ids)):
		print(product_ids[i])
	print("Starting Monitor...")
	time.sleep(3)

	while True:
		monitor(product_ids)
		used_counter()
		time.sleep(60)

