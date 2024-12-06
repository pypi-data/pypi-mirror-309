import time

import pandas as pd

from prophecy_lineage_extractor import messages
from prophecy_lineage_extractor.constants import OUTPUT_PATH, SLEEP_TIME
from prophecy_lineage_extractor.utils import save_excel_file
import logging


def _get_dataset_from_summary_view(json_msg):
    logging.warning("viewType is summaryView, getting datasets")
    # Step 2: Extract all datasets from `processes`
    processes = (
        json_msg.get("params", {})
        .get("lineage", {})
        .get("graph", {})
        .get("processes", {})
    )
    # Filter out all entries with component "Dataset" and collect their names
    datasets = [
        info["id"] for info in processes.values() if info.get("component") == "Dataset"
    ]
    return datasets


def _get_lineage_from_detailed_view(data):
    logging.warning("viewType is detailedDatasetView, getting lineage")
    # Access columns data
    columns = data.get("value", {}).get("dataset", {}).get("columns", [])
    datasetId = data.get("value", {}).get("dataset", {}).get("id", "NA")
    # Extract lineage information for each column
    # Prepare data for DataFrame
    lineage_data = []

    for column in columns:
        column_name = column.get("name")
        # to at least add one row for every column
        lineage_data.append(
            {
                "dataset_id": str(datasetId).split("/")[2],
                "column_name": column_name,
                "upstream_transformation": "",
                # "downstream_transformation": ""
            }
        )

        # Upstream transformations
        for upstream in column.get("upstreamTransformations", []):
            pipeline_name = upstream.get("pipeline", {}).get("name", "Unknown")
            transformations = upstream.get("transformations", [])
            for transformation in transformations:
                process_name = transformation.get("processName", "Unknown")
                transformation_str = transformation.get("transformation", "")
                # upstream_transformation = f"{process_name}: {transformation_str}"
                upstream_transformation = f"{transformation_str}"
                lineage_data.append(
                    {
                        "dataset_id": str(datasetId).split("/")[2],
                        "column_name": column_name,
                        "upstream_transformation": upstream_transformation,
                        # "downstream_transformation": ""
                    }
                )

        # # Downstream transformations
        # for downstream in column.get("downstreamTransformations", []):
        #     pipeline_name = downstream.get("pipeline", {}).get("name", "Unknown")
        #     transformations = downstream.get("transformations", [])
        #     for transformation in transformations:
        #         process_name = transformation.get("processName", "Unknown")
        #         transformation_str = transformation.get("transformation", "")
        #         # downstream_transformation = f"{process_name}: {transformation_str}"
        #         downstream_transformation = f"{transformation_str}"
        #         lineage_data.append({
        #             "dataset_id": str(datasetId).split("/")[2],
        #             "column_name": column_name,
        #             "upstream_transformation": "",
        #             "downstream_transformation": downstream_transformation
        #         })

    # Create a DataFrame
    df = pd.DataFrame(lineage_data)
    save_excel_file(df, OUTPUT_PATH)


def handle_did_open(ws, json_msg):
    logging.warning("Handling didOpen")
    view_type = (
        json_msg.get("params", {})
        .get("lineage", {})
        .get("metaInfo", {})
        .get("viewType")
    )
    if view_type == "summaryView":
        datasets = _get_dataset_from_summary_view(json_msg)
        # for every datasets run and get lineage
        for dataset in datasets:
            # change active entity
            logging.warning(f"running lineage fetch for dataset {dataset}")

            ws.send(messages.change_active_entity(dataset))
            time.sleep(SLEEP_TIME)
            # get lineage
            ws.send(messages.detailed_view())
            time.sleep(SLEEP_TIME)

            logging.warning(f"Going back to summary view")
            ws.send(messages.summary_view())
            time.sleep(SLEEP_TIME)


def handle_did_update(ws, json_msg):
    logging.warning("Handling didUpdate")
    for change in json_msg.get("params", {}).get("changes", []):
        # Check if 'viewType' is present and equals 'detailedDatasetView'
        if (
            change.get("value", {}).get("metaInfo", {}).get("viewType")
            == "detailedDatasetView"
        ):
            # process_detailed_view(change)
            _get_lineage_from_detailed_view(change)
