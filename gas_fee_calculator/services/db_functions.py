import logging 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from elasticsearch import Elasticsearch

#Parameters
ELASTIC_PASSWORD="Q5ncGwb0aEmUXstOVbyX9WcU"
ELASTIC_USERNAME="elastic"
CLOUD_ID="My_deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDNjY2IxZmE4ZDA1MDRlYzlhM2FmYTE4YTFjOGU0YWJkJDdhOGE5YWUwYjNiYjRmNmM4MWZlYzcxOWU5ZDY4ZTgw"
INDEX = "gas-fees-index"

logging.basicConfig(filename="Documentation/logs.txt", level=logging.INFO)

try:
    #Connect to DB
    client = Elasticsearch(
        cloud_id=CLOUD_ID,
        basic_auth=(ELASTIC_USERNAME,ELASTIC_PASSWORD)
    )
    logging.info(" Database connected.") 
except Exception as e:
    logging.critical('Error while connecting to db from db_functions.py: ' + str(e))

#Function that recives documents and returns the result. if an error occurs it logs it in.
def insert_data(document):
    try:
        res = client.index(index = INDEX, body = document)
        if res['result'] == 'created':
            return res
        else:
            logging.error(f'Error inserting the following document: \n {document}')
            return res
    except Exception as e:
        logging.critical('Error in the insert_data function: ' + str(e))

#Function that returns the last month of data that inserted into elasticsearch (by project name), and sorts it by timestamp
def get_last_month_gas_fees(project_name):
    try:
        end_date = datetime.now()
        start_date = end_date - relativedelta(months=1) 

        # Format the start and end dates in ISO format
        start_date_iso = start_date.strftime('%Y-%m-%dT%H:%M:%S')
        end_date_iso = end_date.strftime('%Y-%m-%dT%H:%M:%S')

        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "project_name": project_name
                            }
                        },
                        {
                            "range": {
                                "timestamp": {
                                    "gte": start_date_iso,
                                    "lte": end_date_iso,
                                    "format": "strict_date_optional_time"
                                }
                            }
                        }
                    ]
                }
            }
        }

        search_results = client.search(index=INDEX, body=query, size=744) # max days in a month (31) X  24hours a day

        # Sort the list by the timestamp property
        sorted_objects = sorted(search_results['hits']['hits'], key=extract_timestamp)
        return sorted_objects
    except Exception as e:
        logging.critical('Error in get_last_month_gas_fees function: ' + str(e) )

#function to extract and convert the timestamp string to a datetime object
def extract_timestamp(obj):
    return datetime.fromisoformat(obj["_source"]["timestamp"])
