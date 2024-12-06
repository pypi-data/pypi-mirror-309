import argparse
import json
import logging
import threading
import time
from datetime import datetime, timedelta

import websocket

from prophecy_lineage_extractor import messages
from prophecy_lineage_extractor.constants import (
    # PROJECT_ID,
    # PIPELINE_IDS,
    SLEEP_TIME,
    OUTPUT_PATH,
    PROPHECY_PAT,
    PROPHECY_WS_URL,
)
from prophecy_lineage_extractor.utils import (
    delete_file,
    safe_env_variable,
    send_excel_email,
)
from prophecy_lineage_extractor.ws_handler import handle_did_open, handle_did_update

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Define the format
    datefmt="%Y-%m-%d %H:%M:%S",  # Optional: customize the date format
)

PROJECT_ID = None
PIPELINE_ID = None
last_meaningful_message_time = datetime.now()


def on_error(ws, error):
    logging.error("Error: " + str(error))
    ws.close()
    exit(1)


def on_close(ws, close_status_code, close_msg):
    logging.info("### closed ###")


def on_message(ws, message):
    global last_meaningful_message_time
    logging.info(f"\n\n### RECEIVED a message### ")
    try:
        json_msg = json.loads(message)
        if "method" in json_msg:
            method = json_msg["method"]
            logging.warning(f"method: {method}")
            if method == "properties/didOpen":
                handle_did_open(ws, json_msg)
                last_meaningful_message_time = datetime.now()
                logging.warning(
                    f"[MONITORING]: Updating last_meaningful_message_time "
                    f"={datetime.now()- last_meaningful_message_time}"
                )
            elif method == "properties/didUpdate":
                handle_did_update(ws, json_msg)
                last_meaningful_message_time = datetime.now()
                logging.warning(
                    f"[MONITORING]: Updating last_meaningful_message_time "
                    f"={datetime.now()- last_meaningful_message_time}"
                )
        else:
            raise Exception("method is not found in message", json_msg)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON message: {e}")
        raise e


def on_open(ws):
    delete_file(OUTPUT_PATH)
    logging.info(f"\n\n### SENDING INIT PIPELINE for {PIPELINE_ID} ### ")
    ws.send(messages.init_pipeline(PROJECT_ID, PIPELINE_ID))
    time.sleep(SLEEP_TIME * 10)


def monitor_ws(ws):
    logging.warning("Monitor thread started.")

    """Monitor the WebSocket connection and terminate if inactive."""
    global last_meaningful_message_time
    time.sleep(10)
    while ws.keep_running:
        # logging.warning("Monitoring...")
        if datetime.now() - last_meaningful_message_time > timedelta(seconds=60):
            logging.info(
                "[MONITORING]: No meaningful messages received in the last 5 seconds, "
                "sending mail and Closing WebSocket."
            )
            try:
                send_excel_email(OUTPUT_PATH)
            except Exception as e:
                print(e)
                raise e
            finally:
                ws.close()
        else:
            logging.warning(
                f"[MONITORING]: Meaningful message received {datetime.now() - last_meaningful_message_time} seconds ago"
            )
        time.sleep(5)

    logging.warning("Monitor thread ended.")


def run_websocket():
    """Run WebSocket in a separate thread."""
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        safe_env_variable(PROPHECY_WS_URL),
        header={"X-Auth-Token": safe_env_variable(PROPHECY_PAT)},
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_ws, args=(ws,), daemon=True)
    monitor_thread.start()

    # Start the WebSocket connection
    ws.run_forever()
    return ws


def main():
    parser = argparse.ArgumentParser(description="Prophecy Lineage Extractor")
    # Adding arguments
    parser.add_argument(
        "--project-id", type=str, required=True, help="Prophecy Project ID"
    )
    parser.add_argument(
        "--pipeline-id", type=str, required=True, help="Prophecy Pipeline ID"
    )
    # parser.add_argument("--timezone", type=str, default="UTC", help="Timezone (default: UTC).")

    # Parse arguments
    args = parser.parse_args()

    # Access arguments
    global PROJECT_ID, PIPELINE_ID
    PROJECT_ID = args.project_id
    PIPELINE_ID = args.pipeline_id

    logging.info("Starting WebSocket thread..")
    ws_thread = threading.Thread(target=run_websocket, daemon=True)
    ws_thread.start()
    ws_thread.join()


if __name__ == "__main__":
    main()
