import logging
import os
from typing import Any
from urllib.parse import quote_plus

from mongoengine import connect

logger = logging.getLogger(__name__)


class MongoDBConnectionError(Exception):
    """Custom exception for MongoDB connection errors"""

    pass


def get_ssl_config() -> dict[str, Any]:
    # Optional: TLS configuration
    # https://pymongo.readthedocs.io/en/3.5.1/examples/tls.html#basic-configuration
    tls_config = {}
    if bool(int(os.getenv("MONGODB_TLS", "0"))):
        tls_config.update(
            {
                "tls": True,
                "tlsAllowInvalidCertificates": bool(
                    int(os.getenv("MONGODB_TLS_ALLOW_INVALID_CERTS", "0"))
                ),
                "tlsCAFile": os.getenv("MONGODB_TLS_CA_FILE"),
                "tlsCertificateKeyFile": os.getenv("MONGODB_TLS_CERT_KEY_FILE"),
                "tlsCertificateKeyFilePassword": os.getenv(
                    "MONGODB_TLS_CERT_KEY_FILE_PASSWORD"
                ),
            }
        )

        # Remove None values
        tls_config = {k: v for k, v in tls_config.items() if v is not None}
    return tls_config


def connect_to_mongodb(alias: str = "default") -> Any:
    try:
        db_config = {
            "db": os.getenv("MONGODB_DB", "project1"),
            "host": os.getenv("MONGODB_HOST", "localhost"),
            "port": int(os.getenv("MONGODB_PORT", 27017)),
            "username": os.getenv("MONGODB_USERNAME"),
            "password": quote_plus(os.getenv("MONGODB_PASSWORD", "")),
            "authentication_source": os.getenv("MONGODB_AUTH_SOURCE", "admin"),
            "alias": alias,
            "uuidRepresentation": "standard",
        }
        # Add SSL configuration if enabled
        db_config.update(get_ssl_config())
        # Remove None values to use MongoDB defaults
        db_config = {k: v for k, v in db_config.items() if v is not None}

        # Establish connection
        connection = connect(**db_config)
        # Test connection
        connection.server_info()
        logger.info(
            f"Successfully connected to MongoDB database: {db_config['db']} on {db_config['host']}"
        )
        return connection
    except Exception as e:
        error_msg = f"Failed to connect to MongoDB: {str(e)}"
        logger.error(error_msg)
        raise MongoDBConnectionError(error_msg) from e


def get_connection_string() -> str:
    host = os.getenv("MONGODB_HOST")
    port = os.getenv("MONGODB_PORT")
    db = os.getenv("MONGODB_DB")
    return f"mongodb://{host}:{port}/{db}"


if __name__ == "__main__":
    try:
        MONGODB_CONNECTION = connect_to_mongodb()
        logger.info(f"MongoDB connected at: {get_connection_string()}")
    except MongoDBConnectionError as e:
        logger.critical(f"Could not establish MongoDB connection: {str(e)}")
        raise
