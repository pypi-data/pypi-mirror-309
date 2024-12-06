from psycopg2.extras import Json,execute_values
from datetime import datetime, timezone
from .logManager import *
from .db_credentials import DB_CONFIG
def handle_wallet_signatures(creator_wallet):
    """
    Handles checking, inserting, or updating wallet and signature data.
    """
    signatures = get_signatures(creator_wallet)

    # Convert signatures into a list of strings (PostgreSQL-compatible array format)
    signature_list = [entry['signature'] for entry in signatures]

    # Query to check if wallet address exists
    check_query = """
    SELECT id, signature, signatures FROM transaction_logs
    WHERE user_address = %s;
    """
    
    # Insert/Update queries
    insert_query = """
    INSERT INTO transaction_logs (
        user_address, signature, signatures, timestamp
    )
    VALUES (%s, %s, %s, %s)
    RETURNING *;
    """
    
    update_query = """
    UPDATE transaction_logs
    SET signatures = COALESCE(signatures, %s)
    WHERE id = %s
    RETURNING *;
    """

    results = []

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                # Check if the wallet address exists in the database
                cur.execute(check_query, (creator_wallet,))
                rows = cur.fetchall()

                if rows:
                    # If the wallet exists, check and update signatures
                    for row in rows:
                        row_id, existing_signature, existing_signatures = row
                        if not existing_signatures:
                            # Update if signatures are missing
                            cur.execute(update_query, (signature_list, row_id))
                            updated_row = cur.fetchone()
                            results.append(updated_row)
                        else:
                            # Signatures already exist
                            results.append(row)
                else:
                    # Wallet address not found; insert a new row
                    cur.execute(
                        insert_query,
                        (creator_wallet, None, signature_list, datetime.now(timezone.utc)),
                    )
                    new_row = cur.fetchone()
                    results.append(new_row)

                conn.commit()

    except Exception as e:
        print(f"Error handling wallet signatures: {e}")

    return results
def insert_transaction_log(data):
    """
    Inserts or updates a transaction log in the database.
    """
    # Provide default values for any missing keys
    default_data = {
        "signature": None,
        "mint": None,
        "sol_amount": None,
        "token_amount": None,
        "is_buy": None,
        "user_address": None,
        "timestamp": datetime.now(timezone.utc),  # Use current time with timezone awareness
        "virtual_sol_reserves": None,
        "virtual_token_reserves": None,
        "metadata": None,
        "logNotification": None,
        "signatures": None,
        "transaction": None
    }
    # Merge with provided data
    default_data.update(data)

    # Convert `timestamp` to datetime if it's an integer (Unix timestamp)
    if isinstance(default_data["timestamp"], int):
        default_data["timestamp"] = datetime.fromtimestamp(default_data["timestamp"], tz=timezone.utc)

    query = """
    INSERT INTO transaction_logs (
        signature, mint, sol_amount, token_amount, is_buy, user_address, 
        timestamp, virtual_sol_reserves, virtual_token_reserves, metadata, 
        logNotification, signatures, transaction
    )
    VALUES (
        %(signature)s, %(mint)s, %(sol_amount)s, %(token_amount)s, %(is_buy)s, %(user_address)s, 
        %(timestamp)s, %(virtual_sol_reserves)s, %(virtual_token_reserves)s, %(metadata)s, 
        %(logNotification)s, %(signatures)s, %(transaction)s
    )
    ON CONFLICT (signature) DO UPDATE SET
        mint = COALESCE(EXCLUDED.mint, transaction_logs.mint),
        sol_amount = COALESCE(EXCLUDED.sol_amount, transaction_logs.sol_amount),
        token_amount = COALESCE(EXCLUDED.token_amount, transaction_logs.token_amount),
        is_buy = COALESCE(EXCLUDED.is_buy, transaction_logs.is_buy),
        user_address = COALESCE(EXCLUDED.user_address, transaction_logs.user_address),
        timestamp = COALESCE(EXCLUDED.timestamp, transaction_logs.timestamp),
        virtual_sol_reserves = COALESCE(EXCLUDED.virtual_sol_reserves, transaction_logs.virtual_sol_reserves),
        virtual_token_reserves = COALESCE(EXCLUDED.virtual_token_reserves, transaction_logs.virtual_token_reserves),
        metadata = COALESCE(EXCLUDED.metadata, transaction_logs.metadata),
        logNotification = COALESCE(EXCLUDED.logNotification, transaction_logs.logNotification),
        signatures = COALESCE(EXCLUDED.signatures, transaction_logs.signatures),
        transaction = COALESCE(EXCLUDED.transaction, transaction_logs.transaction);
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(query, {key: Json(value) if key in ['metadata', 'logNotification', 'transaction'] else value
                                    for key, value in default_data.items()})
                conn.commit()
                print(f"Transaction log inserted/updated successfully. for {list(data.keys())}")
    except Exception as e:
        print(f"Error inserting transaction log: {e}")

def fetch_transaction_logs(limit=10, offset=0, filters=None):
    """
    Fetches transaction logs from the database with optional filters and offset.
    
    :param limit: The maximum number of rows to fetch.
    :param offset: The starting point for fetching rows.
    :param filters: A dictionary of column-value pairs to filter the logs.
    :return: A list of dictionaries containing the transaction log details.
    """
    query = """
    SELECT signature, mint, sol_amount, token_amount, is_buy, user_address, 
           timestamp, virtual_sol_reserves, virtual_token_reserves, metadata, 
           logNotification, signatures, transaction
    FROM transaction_logs
    """
    
    where_clause = []
    params = []

    # Add filters dynamically
    if filters:
        for column, value in filters.items():
            where_clause.append(f"{column} = %s")
            params.append(value)

    # Add WHERE clause if filters exist
    if where_clause:
        query += " WHERE " + " AND ".join(where_clause)
    
    # Add ORDER BY, LIMIT, and OFFSET
    query += " ORDER BY timestamp DESC LIMIT %s OFFSET %s;"
    params.extend([limit, offset])

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(query, tuple(params))
                results = cur.fetchall()
                colnames = [desc[0] for desc in cur.description]
                return [dict(zip(colnames, row)) for row in results]
    except Exception as e:
        print(f"Error fetching transaction logs: {e}")
        return []
def insert_into_table(query,data=None):
    try:
        # Connect to the database
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                # Execute the query
                if data is not None:
                    cur.execute(query, data)
                else:
                    cur.execute(query)
                conn.commit()
                print(f"Transaction log inserted/updated successfully for {list(data.keys())}")
    except Exception as e:
        print(f"Error inserting transaction log: {e}")

