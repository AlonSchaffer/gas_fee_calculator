import logging

logging.basicConfig(filename="Documentation/logs.txt", level=logging.INFO)

# Geets gwei and returns it in eth
def gwei_to_eth(gwei_value):
    try:        
        return gwei_value / 10**9
    except Exception as e:
        logging.critical('Error in gwei_to_eth function: ' + str(e)) 

# Gets eth and returns it in usd with the current exchange.
def eth_to_usd(current_exchange, eth):
    try:        
        return (eth * current_exchange)
    except Exception as e:
        logging.critical('Error in eth_to_usd function: ' + str(e))