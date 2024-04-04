from sqlalchemy import create_engine
from psycopg2 import connect
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
dbname = os.getenv('DATABASE')


print('Connecting to the PostgreSQL database')
conn = connect(user=user, password=password, host=host, port=port, dbname=dbname)
print('Connection successful')
print('Creating an engine')
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}')
print('Engine created')

cursor = conn.cursor()
print('Creating table')
cursor.execute('''
DROP TABLE IF EXISTS walmart_ecommerce_product_details;
CREATE TABLE walmart_ecommerce_product_details
(
    id SERIAL NOT NULL,
    source_unique_id CHAR(32) NOT NULL,
    crawl_timestamp VARCHAR(50) NOT NULL,
    product_url VARCHAR(200) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    description TEXT,
    list_price DECIMAL(18, 10),
    sale_price DECIMAL(18, 10),
    brand VARCHAR(500),
    item_number BIGINT,
    gtin BIGINT,
    package_size VARCHAR(500),
    category VARCHAR(1000),
    postal_code VARCHAR(10),
    available VARCHAR(10) NOT NULL,
    embedding TEXT
);
               ''')
print('Table created')

df = pd.read_csv('walmart-product-with-embeddings-dataset-usa.csv')
print(df.head())
print('Loading data into SQL database')
df.to_sql('walmart_ecommerce_product_details', con=engine, if_exists='append', index=False, chunksize=10000)
conn.commit()
conn.close()
cursor.close()
engine.dispose()