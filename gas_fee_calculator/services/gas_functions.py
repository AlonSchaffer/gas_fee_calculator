import logging
from datetime import datetime
from services.scrapping_functions import get_avg_gas_fee
from services.db_functions import insert_data 

logging.basicConfig(filename="Documentation/logs.txt", level=logging.INFO)

#The function retrieves the average Gas fee from each project and sends the data to elasticsearch db.
def get_data_from_projects():
    try:
        logging.info('Starting get_data_from_projects function..')

        gas_fee_data = get_avg_gas_fee()
        for data in gas_fee_data:
            document = {
                "project_name" : data['project_name'],
                "average_gas_fee_eth" : data["avg_gas_fee_eth"],
                "average_gas_fee_usd" : data["avg_gas_fee_usd"],
                "hour" : datetime.now().hour,
                "timestamp" : datetime.now(),
            }
            insert_data(document)
        logging.info('ENDED get_data_from_projects')

    except Exception as e:
        logging.critical("Error at get_data_from_projects function: " + str(e))