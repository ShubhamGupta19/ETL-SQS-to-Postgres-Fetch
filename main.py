import logging
from aws import sqs
from database import postgres
from utils import pii_masking
import config
table_name = 'user_logins'
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def main():
    try:
        setup_logging()

        # Step 1: Set Up Docker Environment (Run LocalStack and Postgres containers)
     

        # Step 2: Read Data from AWS SQS Queue
        logging.info("Reading data from AWS SQS Queue...")
        sqs_queue_name = config.SQS_QUEUE_NAME
        data = sqs.read_data_from_sqs(sqs_queue_name)

        # Step 3: Transform the Data
        logging.info("Transforming the data...")
        transformed_data = pii_masking.mask_pii_data(data)

        if not postgres.check_table_exists(table_name):
            postgres.create_user_logins_table()
       


        # Step 4: Write to Postgres Database
        logging.info("Writing data to Postgres Database...")
        postgres.write_to_postgres(transformed_data)

        logging.info("Data processing and writing to Postgres completed successfully!")

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        # You may choose to log the error or send an alert/notification here.

if __name__ == "__main__":
    main()