import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime
from dhooks import Webhook, Embed
from threading import Thread

blacklist = ['AK 9', 'ID 8', 'MT 5', 'ND 5', 'SC 2', 'WV 2', 'VT 0', 'TN 3']

def productInfo(sku):
	link = "https://www.target.com/p/-/A-{}".format(sku)
	page = requests.get(link)
	soup = BeautifulSoup(page.text, 'html.parser')
	title = soup.find('title').text
	if title.endswith(': Target'):
		title = title[:-8]
	images = soup.find_all('img')
	image_url = (images[0]['src'])
	return title, image_url

def webhook(sku, name, address, quantity, ctg):
	link = r'https://www.target.com/p/-/A-{}'.format(sku)
	info = productInfo(sku)
	title = info[0]
	productImage = info[1]

	if ctg == 'CA':
		hook = Webhook('https://discordapp.com/api/webhooks/720101337957662780/NRm2Kd0SM9WmokNBvlM_gHMsD1cgSrr9_JggudA6I14-uy1-4YJtWDU9kHK6pG4E5itu')
	elif ctg == 'NY':
		hook = Webhook('https://discordapp.com/api/webhooks/720101888430964796/0tzMyXEtw8K_N4w1s_OEuywsaOb4KdkmWfPmS_Gt4QOILaNNVuQC2bpTs7193rLL7EDt')
	elif ctg == 'TX':
		hook = Webhook('https://discordapp.com/api/webhooks/720327986116558878/NrdktaWHsJZdWo7q0vRnZKLgPKIYsZyQLvcHg-qm6U4bsQHeHf5s5v6mTRZa81Vl8W06')
	else:
		hook = Webhook('https://discordapp.com/api/webhooks/706970539071242292/6gH5YHCF3UNDz8fwoe2gsiE-7qhG3nNVBpnpiMVTIqttnUUwRdQXtr4F2ej7He3VfO84')
	
	priv_hook = Webhook('https://discordapp.com/api/webhooks/704859631851274301/ZN2Z2vopiyFjD2LEc9n_538d9eIXdXai6pZyXlZKlg33_ZKD6pH1H7a1DJVecLWm1vdJ')

	embed = Embed(
	    description="[Store Pickup](" + link + ")",
	    color=0x1ab83c,
	    timestamp='now'
	    )

	embed.set_author(name=title, icon_url=None, url=link)
	embed.add_field(name='Store:', value=name, inline=True)
	embed.add_field(name='Quantity:', value=str(quantity), inline=True)
	embed.add_field(name='Address:', value=address, inline=False)

	embed.set_footer(text='created by enrique#2519', icon_url='https://cdn.discordapp.com/avatars/267782036893204481/58904351e4e12eec9302b22cd6b209d9.webp?size=256')

	embed.set_thumbnail(productImage)
	#embed.set_image(image2)

	hook.send(embed=embed)
	priv_hook.send(embed=embed)


def checkProduct(sku):
	monitor = requests.get("https://api.target.com/fulfillment_aggregator/v1/fiats/{}?key=eb2551e4accc14f38cc42d32fbc2b2ea&nearby=94404&limit=20&requested_quantity=1&radius=5000&include_only_available_stores=true&fulfillment_test_mode=grocery_opu_team_member_test".format(sku))
	res = monitor.json()
	locations = res['products'][0]['locations']
	for location in locations:
		name = location['store_name']
		address = location['store_address']
		quantity = location['location_available_to_promise_quantity']
		print("[{}]\t[{}]".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), sku), end=" ")
		if location['order_pickup']['availability_status'] == "IN_STOCK":
			print("%-30s: IN_STOCK" % (name))
			if not any(s in name for s in cool_list):
				if not any(s in address for s in blacklist):

					if 'CA 9' in address:
						webhook(sku, name, address, int(quantity), "CA")
					elif 'NY 1' in address:
						webhook(sku, name, address, int(quantity), "NY")
					elif 'TX 7' in address:
						webhook(sku, name, address, int(quantity), "TX")
					else:
						webhook(sku, name, address, int(quantity), None)
					cool_list.append(name)
					time.sleep(0.5)
		else:
			print("%-30s: OUT_OF_STOCK" % (name))

def cooldown():
	global cool_list
	global count

	if count > 19:
		cool_list = []
		count = 0
	count += 1


def run(sku):
	while True:
		checkProduct(sku)
		cooldown()
		time.sleep(60)

cool_list = []
count = 0

if __name__ == '__main__':
	products = [
	16747574,
	77428670,
	54005460,
	54007754
	]

	print("""\
███████╗███╗   ██╗██████╗ ██╗ ██████╗ ██╗   ██╗███████╗
██╔════╝████╗  ██║██╔══██╗██║██╔═══██╗██║   ██║██╔════╝
█████╗  ██╔██╗ ██║██████╔╝██║██║   ██║██║   ██║█████╗  
██╔══╝  ██║╚██╗██║██╔══██╗██║██║▄▄ ██║██║   ██║██╔══╝  
███████╗██║ ╚████║██║  ██║██║╚██████╔╝╚██████╔╝███████╗
╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝ 
                                                       """)
	loop = input("Press any key to start...")
	for product in products:
		t = Thread(target=run, args=(product,))
		t.start()
		time.sleep(0.5)
