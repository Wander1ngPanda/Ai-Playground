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
                ''')
conn.commit()
cursor.execute('''
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
conn.commit()
print('Table created')

df = pd.read_csv('local_data/walmart-product-with-embeddings-dataset-usa.csv')
print(df.head())
print('Loading data into SQL database')
df.to_sql('walmart_ecommerce_product_details', con=engine, if_exists='append', index=False, chunksize=10000)
conn.commit()

print('Data loaded successfully')

print('Creating table')
cursor.execute('''
DROP TABLE IF EXISTS evolution_dataset;
                ''')
conn.commit()
cursor.execute('''
CREATE TABLE evolution_dataset
(
    Genus_and_Species VARCHAR(255),
    Time DECIMAL(18, 8),
    Location VARCHAR(255),
    Zone VARCHAR(255),
    Current_Country VARCHAR(255),
    Habitat VARCHAR(255),
    Cranial_Capacity DECIMAL(18, 8),
    Height DECIMAL(18, 8),
    Incisor_Size VARCHAR(255),
    Jaw_Shape VARCHAR(255),
    Torus_Supraorbital VARCHAR(255),
    Prognathism VARCHAR(255),
    Foramen_Magnum_Position VARCHAR(255),
    Canine_Size VARCHAR(255),
    Canine_Shape VARCHAR(255),
    Tooth_Enamel VARCHAR(255),
    Tecno VARCHAR(255),
    Tecno_type VARCHAR(255),
    biped VARCHAR(255),
    Arms VARCHAR(255),
    Foots VARCHAR(255),
    Diet VARCHAR(255),
    Sexual_Dimorphism VARCHAR(255),
    Hip VARCHAR(255),
    Vertical_Front VARCHAR(255),
    Anatomy VARCHAR(255),
    Migrated VARCHAR(255),
    Skeleton VARCHAR(255)
);
               ''')
conn.commit()
print('Table created')

df = pd.read_csv('local_data/Evolution_DataSets.csv')
print(df.head())
print(df.info())
print('Loading data into SQL database')
df.to_sql('evolution_dataset', con=engine, if_exists='replace', index=False, chunksize=10000)
conn.commit()



conn.close()
cursor.close()
engine.dispose()

