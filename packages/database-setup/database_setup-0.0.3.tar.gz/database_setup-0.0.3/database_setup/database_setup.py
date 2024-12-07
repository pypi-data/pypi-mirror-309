"""
Database Setup Module

This module provides functionalities to configure, initialize, and manage the database setup. 
It includes methods for loading configuration, creating a database, setting up connection pools, 
executing SQL scripts, and inserting default admin users.

Dependencies:
- os
- yaml
- pymysql
- dbutils.pooled_db
- logging
- Crypto (for password encryption)

Author: Komal Swami
Date: 2024-11-20
"""
import os
import yaml
import pymysql
from pathlib import Path
from dbutils.pooled_db import PooledDB
import logging
import pymysql
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
BLOCK_SIZE = 32

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def load_config(config):
    """
    Load the database configuration from a YAML file.

    Args:
        config (str): Path to the project directory.

    Returns:
        dict: Database configuration for the development environment.
    """
    config_file = os.path.join(config,'config', 'database.yml')
    
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config['development']

def create_database_if_not_exists(connection, database_name):
    """
    Create the database if it does not already exist.
    
    Args:
        connection (pymysql.connections.Connection): Connection to the MySQL server.
        database_name (str): Name of the database to create.
    """
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    logging.info(f"Database '{database_name}' created or already exists.")
    cursor.close()

def initialize_database(config):
    """
    Initialize the database connection pool.
    
    Args:
        config (dict): Database configuration.
    
    Returns:
        PooledDB: Database connection pool.
    """
    pool = PooledDB(
        creator=pymysql,
        host=config['host'],
        port=config['port'],
        user=config['username'],
        password=config['password'],
        database=config['database'],
        autocommit=config['autocommit'],
        blocking=config['blocking'],
        maxconnections=config['maxconnections'],
    )
    logging.info(f"Database connection pool created for '{config['database']}'.")
    return pool

def execute_sql_file(connection, file_path):
    """
    Execute a SQL file on the database.
    
    Args:
        connection (pymysql.connections.Connection): Connection to the database.
        file_path (str): Path to the SQL file.
    """
    cursor = connection.cursor()
    with open(file_path, 'r') as file:
        queries = file.read().split(';\n')
        for query in queries:
            if query.strip():
                cursor.execute(query)
    connection.commit()
    cursor.close()
    logging.info(f"Executed SQL file: {file_path}")

def encrypt_password(plaintext, key=b"1234567890123456"):
    """
    Encrypt the password using AES.
    """
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = base64.b64encode(
        cipher.encrypt(pad(plaintext.encode("utf-8"), BLOCK_SIZE))
    ).decode("utf-8")
    return encrypted

def insert_admin_user(connection):
    """
    Insert default admin user into the `User` table with an encrypted password.
    """
    admin_data = {
        "user_type": "admin",
        "name": "Default Admin",
        "username": "admin",
        "email": "info@yun.buzz",
        "mobile": "8888888888",
        "password": "admin",  
        "user_access": 1,
    }
    encrypted_password = encrypt_password(admin_data["password"])

    # SQL query to insert the admin user
    insert_query = """
        INSERT INTO `User` (user_type, name, username, email, mobile, password, user_access)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    data_tuple = (
        admin_data["user_type"],
        admin_data["name"],
        admin_data["username"],
        admin_data["email"],
        admin_data["mobile"],
        encrypted_password,
        admin_data["user_access"],
    )

    cursor = connection.cursor()
    try:
        cursor.execute(insert_query, data_tuple)
        connection.commit()
        logging.info("Admin user inserted successfully.")
    except Exception as e:
        connection.rollback()
        logging.error(f"Failed to insert admin user: {e}")
    finally:
        cursor.close()
        
def setup_database(config_dir):
    """
    Args project dir path
    Setup the database by creating the database, initializing the connection pool, 
    and executing the schema and seed SQL files.
    """
    logging.info("Loading configuration...")
    
    config = load_config(config_dir)
    
    logging.info("Connecting to MySQL server...")
    temp_connection = pymysql.connect(
        host=config['host'],
        user=config['username'],
        password=config['password'],
        port=config['port'],
    )
    
    logging.info("Creating database if not exists...")
    create_database_if_not_exists(temp_connection, config['database'])
    temp_connection.close()
    
    logging.info("Initializing database connection pool...")
    pool = initialize_database(config)
    connection = pool.connection()
    
    logging.info("Executing schema SQL file...")
    schema_file_path = os.path.join(config_dir, 'config', 'schema.sql')
    execute_sql_file(connection, schema_file_path)
    
    logging.info("Creating admin user...")
    insert_admin_user(connection)
    
    logging.info("Executing seed SQL file...")
    seed_file_path = os.path.join(config_dir, 'config', 'seed.sql')
    execute_sql_file(connection, seed_file_path)
    
    
    
    connection.close()
    logging.info("Database setup completed successfully.")