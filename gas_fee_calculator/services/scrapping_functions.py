import logging
import requests
from services.financial_functions import gwei_to_eth , eth_to_usd

API_KEY = "WXAK8JUP9YUEXMTKI35IXQ62S29PRMA2WU"
ADDRESSES = [ ("Cryptopunks" , "0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB"), ("Mutantape" , "0x60e4d786628fea6478f785a6d7e704777c86a7c6")] # Cryptopunks && Mutantape
HEADERS = {'User-Agent': 'Mozilla'}
COINGECKO_URL = "https://www.coingecko.com/price_charts/279/usd/90_days.json"

logging.basicConfig(filename="Documentation/logs.txt", level=logging.INFO)

#This function scraps from the etherscan api the last logs for each project in the addresses list and calculates the gas fee for each of the last 1000 transactions.
#Then calculates the average amount of gas fee for this project and returns the data.
def get_avg_gas_fee():
    try:
        # Get current exchange for ETH to USD
        current_exchange = requests.get(COINGECKO_URL, headers=HEADERS).json()["stats"][-1][1]
        data = []

        # Get the avg gas fee per address (1000 last logs)
        for address in ADDRESSES:
            counter = 0
            total_amount_eth = 0
            url = f"https://api.etherscan.io/api?module=logs&action=getLogs&address={address[1]}&apikey={API_KEY}"
            res = requests.get(url).json()
            for log in res['result']:

                gp_gwei_value = int(log['gasPrice'], 16)
                gu_gwei_value = int(log["gasUsed"], 16)

                # Gas price (ETH) X Gas used(ETH) X current exchange = gas fee
                total_amount_eth += gwei_to_eth(gu_gwei_value) * gwei_to_eth(gp_gwei_value)
                counter += 1
            data.append({
                "project_name" : address[0],
                "avg_gas_fee_usd" : float(eth_to_usd(current_exchange, total_amount_eth / counter)), 
                "avg_gas_fee_eth" : float(total_amount_eth / counter)})
        return data
    except Exception as e:
        logging.critical('ERROOR in start.py: ' + str(e) + '\n' ) 
        