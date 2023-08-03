# Fetch Rewards Data Engineering ETL Application
### Project Description
The Fetch Rewards Data Engineering ETL (Extract, Transform, Load) application is designed to read JSON data from an AWS SQS (Simple Queue Service) queue, perform data transformation to mask sensitive information, and then write the processed data to a PostgreSQL database. The application is developed using Python and utilizes several libraries and tools to efficiently handle the data pipeline.

## Tech Stack Used
  1. Programming Language: Python
  2. Libraries: psycopg2, boto3, awscli-local
  3. Database: PostgreSQL
    
## Infrastructure Required.

  1. Docker: Containerization and deployment
  2. Docker Compose: Defining multi-container environment
  3. Localstack: Emulating local AWS services (SQS)
  4. PostgreSQL: Storing transformed data

### Functional Flow

    1. The aws module interacts with the localstack-based SQS service to read JSON data representing user login behavior.
    2. Data is fetched from the SQS queue, and sensitive fields like device_id and ip are masked to protect user privacy while still allowing duplicate identification.
    3. The transformed data is then passed to the database module, which utilizes psycopg2 to interact with the PostgreSQL database.
    4. If the user_logins table does not exist, the database module creates the table based on the provided DDL (Data Definition Language).
    5. The transformed records are inserted into the user_logins table within the PostgreSQL database.


### Step 1: Clone the repository
```bash
git clone https://github.com/ShubhamGupta19/ETL-SQS-to-Postgres-Fetch.git
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n fetch python=3.7.6 -y
```

```bash
conda activate fetch
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```

### Step 4 - Insert Values in the config.py file
```bash
# Configuration settings
SQS_QUEUE_NAME = #######
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = #######
DB_PASSWORD = ######

```

### Step 5. - Launch the application along with localstack and PostgreSQL containers 
```bash
docker-compose up -d
```

### Step 6. - Run the ETL Script
```bash
python main.py
```
### Step 7. Testing Local Access
To retrieve a message from the queue, utilize the awslocal tool:
  ```
  awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
  ```
To establish a connection with the PostgreSQL database and confirm the table's existence, execute the following command:
  ```
  psql -d postgres -U postgres -p 5432 -h localhost -W
  ```
Afterward, run the subsequent SQL command:
```
  SELECT * FROM user_logins;
  ```


## Directory Structure
```bash
FetchApp/
├── aws/
│   ├── __init__.py                # Package for AWS related functions and utilities
│   ├── sqs.py                     # Module for reading data from AWS SQS Queue
├── database/
│   ├── __init__.py                # Package for database related functions and utilities
│   ├── postgres.py                # Module for writing data to PostgreSQL database
├── utils/
│   ├── __init__.py                # Package for general utility functions
│   └── pii_masking.py             # Module containing functions for PII masking
├── config.py                      # Configuration file with database and AWS settings
├── docker-compose.yml             # Docker Compose configuration for running test environment
├── Dockerfile                     # Dockerfile for building the application image
├── requirements.txt               # List of Python dependencies
└── main.py                        # Main script to execute the ETL process


```

## Next Steps
If additional time were available, the project could be expanded with the following improvements:

    1. Implementing a more robust error handling mechanism for handling exceptions during data processing and database interactions.
    2. Enhancing data validation to ensure the correctness of input JSON data.
    3. Scaling the application for larger datasets by optimizing data processing and introducing parallel processing techniques.
    4. Implementing a more secure method for storing database credentials and AWS access keys, such as using environment variables or configuration files.
    5. Writing testing files for each and every module.

## Deployment and Production-Ready Considerations:

    1. For production deployment, the application can be containerized and orchestrated using Kubernetes for efficient scaling and management.
    2. Additional monitoring and alerting systems can be implemented to track application health and performance.
    3. An infrastructure-as-code (IaC) approach using tools like Terraform can be adopted for automating the setup of AWS resources in a production environment.
    4. The application can be further optimized for handling high-volume data and processing real-time data streams.

## Assumptions
    1. The provided data in the SQS queue follows a specific JSON schema and contains the necessary fields for processing.
    2. The PostgreSQL database credentials are accessible and correct for establishing a connection.
    3. Localstack simulates the AWS SQS service adequately for local testing and development.
    

