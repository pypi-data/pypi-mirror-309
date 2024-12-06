from .utils import get_socket_url,get_websocket_params
from .programData import *
from .db_credentials import DB_CONFIG,RABBIT_CONFIG
from .logManager import *
import pika,logging,threading,websockets,asyncio
logger = logging.getLogger(__name__)
def process_websocket_message(message):
    """
    Process an individual WebSocket message.
    """
    try:
    # Confirm and retrieve log by signature
        logNotification = log_mgr.confirm_log(logNotification=message)
        if not logNotification:
            raise ValueError("Invalid or empty logNotification")

        signature = get_signature_from_log(log=logNotification)
        if not signature:
            raise ValueError("Missing signature in logNotification")

        # Parse program data
        all_js = get_program_data(logNotification, {"signature": signature})
        if not all_js:
            raise ValueError("Failed to parse program data from logNotification")

        # Check for 'user_address' in all_js
        user_address = all_js.get('user_address')
        if not user_address:
            raise ValueError("'user_address' not found in parsed data")

        # Insert parsed data and handle wallet signatures
        insert_transaction_log(all_js)
        handle_wallet_signatures(user_address)

        # Fetch from the database for verification
        fetched = fetch_transaction_logs(filters={'user_address': user_address})
        print(f"Fetched logs for user_address {user_address}")



    except Exception as e:
        logger.error(f"Error processing WebSocket message: {e}")
    
# RabbitMQ Consumer
def consume_rabbitmq():
    try:
        connection_params = pika.ConnectionParameters(
            host=RABBIT_CONFIG.get('host'),
            credentials=pika.PlainCredentials(RABBIT_CONFIG.get('user'), RABBIT_CONFIG.get('password'))
        )
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()
        channel.queue_declare(queue=RABBIT_CONFIG.get('queue'), durable=True)

        logger.info(f"Connected to RabbitMQ. Listening on queue: {RABBIT_CONFIG.get('queue')}")

        def callback(ch, method, properties, body):
            logger.info(f"Received RabbitMQ message: {body.decode()}")
            try:
                message_data = json.loads(body)
                logger.info(f"Parsed RabbitMQ message: {message_data}")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse RabbitMQ message: {e}")

            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        channel.basic_consume(queue=RABBIT_CONFIG.get('queue'), on_message_callback=callback)
        channel.start_consuming()

    except Exception as e:
        logger.error(f"Error in RabbitMQ consumer: {e}")
# WebSocket Listener
async def connect_to_websocket():
    """
    Connect to the WebSocket and process incoming messages.
    """
    
    
    while True:
        try:
            async with websockets.connect(get_socket_url()) as websocket:
                await websocket.send(get_websocket_params())
                response = await websocket.recv()
                logger.info(f"Subscribed to logs: {response}")

                async for message in websocket:
                    if get_log_value_from_key(message,'err') == None:
                        process_websocket_message(message)

        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            await asyncio.sleep(5)  # Retry after a short delay
def run_solcatcher():
    rabbitmq_thread = threading.Thread(target=consume_rabbitmq, daemon=True)
    rabbitmq_thread.start()
    asyncio.run(connect_to_websocket())
