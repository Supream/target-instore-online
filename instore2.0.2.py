import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime
from dhooks import Webhook, Embed
from threading import Thread

blacklist = ['AK 9', 'ID 8', 'MT 5', 'ND 5', 'SC 2', 'WV 2', 'VT 0', 'TN 3', 'HI 9']

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
    elif ctg == 'NY/NJ':
        hook = Webhook('https://discordapp.com/api/webhooks/720101888430964796/0tzMyXEtw8K_N4w1s_OEuywsaOb4KdkmWfPmS_Gt4QOILaNNVuQC2bpTs7193rLL7EDt')
    elif ctg == 'TX':
        hook = Webhook('https://discordapp.com/api/webhooks/720327986116558878/NrdktaWHsJZdWo7q0vRnZKLgPKIYsZyQLvcHg-qm6U4bsQHeHf5s5v6mTRZa81Vl8W06')
    elif ctg == 'NC':
        hook = Webhook('https://discordapp.com/api/webhooks/737050681516490773/VU_q-7AwwrBw0QJqis6v_5jIBgtzvLQ6oVoIJCwHxHO33FR1lP_XJ9kYkC2FEVuSP0YM')
    elif ctg == 'PA':
        hook = Webhook('https://discordapp.com/api/webhooks/737050842498334731/Qxho8UyZoK1gTUWa8XeMQgL_01iYldNVzqmk0CbsqnmUZwk2GHb1OcbKn59x7NNoEJM2')
    elif ctg == 'IL':
        hook = Webhook('https://discordapp.com/api/webhooks/737050943253643306/_Rz875PGMJexmitj5-TrjfUGoeFZFiuzIfZ2Kcdh1TGkNE3flhwGUhwh9I79o-rHgXMo')
    elif ctg == 'FL/GA':
        hook = Webhook('https://discordapp.com/api/webhooks/737051030109552660/AH4h36hB5dW0cpwRjyAUGgS26ZtnIhSAzAQUXLm931qIZGk8LOCLISBIGimbeqTq_fnt')
    elif ctg == 'DMV':
        hook = Webhook('https://discordapp.com/api/webhooks/737051138246967386/djfgdX4wwGMk336Ft6t_AGi6JRC3kf7_GG-daJtGRdZxbB3OWsN40KK3aypYKCVTT3GI')
    elif ctg == 'AZ':
        hook = Webhook('https://discordapp.com/api/webhooks/737051222824976525/4Hny5X7XnTF7Ju1aWHydFgppbLvHPH-vAJ1mmb3VW8zCIFnqmfjmh88IHRoOXXuRWi0V')
    elif ctg == 'NEW_ENGLAND':
        hook = Webhook('https://discordapp.com/api/webhooks/737053468967305258/Jdr-apz8eHLub-4BgFmYSW-yruTASWVAYsPOFOzEl8bjVAMry6LSRRKdcmbRYcBu9esJ')
    else:
        hook = Webhook('https://discordapp.com/api/webhooks/706970539071242292/6gH5YHCF3UNDz8fwoe2gsiE-7qhG3nNVBpnpiMVTIqttnUUwRdQXtr4F2ej7He3VfO84')
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
    #priv_hook.send(embed=embed)


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
                    elif 'NY 1' in address or 'NJ 0' in address:
                        webhook(sku, name, address, int(quantity), "NY/NJ")
                    elif 'TX 7' in address:
                        webhook(sku, name, address, int(quantity), "TX")
                    elif 'NC 2' in address:
                        webhook(sku, name, address, int(quantity), "NC")
                    elif 'PA 1' in address:
                        webhook(sku, name, address, int(quantity), "PA")
                    elif 'IL 6' in address:
                        webhook(sku, name, address, int(quantity), "IL")
                    elif 'FL 3' in address or 'GA 3' in address:
                        webhook(sku, name, address, int(quantity), "FL/GA")
                    elif 'DC 2' in address or 'MD 2' in address or 'VA 2' in address:
                        webhook(sku, name, address, int(quantity), "DMV")
                    elif 'AZ 8' in address:
                        webhook(sku, name, address, int(quantity), "AZ")
                    elif 'MA 0' in address or 'RI 0' in address or 'CT 0' in address or 'NH 0' in address:
                        webhook(sku, name, address, int(quantity), "NEW_ENGLAND")
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
		time.sleep(30)

cool_list = []
count = 0

if __name__ == '__main__':
	products = [
	77464001,
	77464002
	#16747574,
	#77428670,
	#54005460,
	#54007754
	]

	print("""\
███████╗███╗   ██╗██████╗ ██╗ ██████╗ ██╗   ██╗███████╗
██╔════╝████╗  ██║██╔══██╗██║██╔═══██╗██║   ██║██╔════╝
█████╗  ██╔██╗ ██║██████╔╝██║██║   ██║██║   ██║█████╗  
██╔══╝  ██║╚██╗██║██╔══██╗██║██║▄▄ ██║██║   ██║██╔══╝  
███████╗██║ ╚████║██║  ██║██║╚██████╔╝╚██████╔╝███████╗
╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝ 
                                                       """)
	print("Target inStore v2.0.2")
	loop = input("Press any key to start...")
	for product in products:
		t = Thread(target=run, args=(product,))
		t.start()
		time.sleep(0.5)
