import json
import logging
import threading
import time

import websocket

from prophecy_lineage_extractor import messages
from prophecy_lineage_extractor.constants import PROJECT_ID, PIPELINE_IDS, SLEEP_TIME, OUTPUT_PATH
from prophecy_lineage_extractor.constants import WS_URL, WS_HEADER
from prophecy_lineage_extractor.utils import delete_file
from prophecy_lineage_extractor.ws_handler import handle_did_open, handle_did_update


def on_error(ws, error):
    logging.error("Error: " + str(error))
    exit(1)


def on_close(ws, close_status_code, close_msg):
    logging.info("### closed ###")


def on_message(ws, message):
    logging.info(f"\n\n### RECEIVED a message### ")
    # print("Raw message received:", message)

    try:
        # Parse the JSON message
        json_msg = json.loads(message)
        if "method" in json_msg:
            method = json_msg["method"]
            logging.warning(f"method: {method}")
            if method == "properties/didOpen":
                # logging.warning("Method: DID OPEN")
                handle_did_open(ws, json_msg)
            elif method == "properties/didUpdate":
                handle_did_update(ws, json_msg)
        else:
            raise Exception("method is not found in message", json_msg)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON message: {e}")
        exit(1)


def on_open(ws):
    def run(*args):
        # delete the output file If exists before starting processing
        delete_file(OUTPUT_PATH)
        for PIPELINE in PIPELINE_IDS:
            PIPELINE_ID = f"{PROJECT_ID}/pipelines/{PIPELINE}"
            logging.info(f"\n\n### SENDING INIT PIPELINE for {PIPELINE_ID} ### ")
            ws.send(messages.init_pipeline(PROJECT_ID, PIPELINE_ID))
            time.sleep(SLEEP_TIME)

    threading.Thread(target=run).start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        WS_URL,
        header=WS_HEADER,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()
