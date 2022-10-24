import pandas as pd
import numpy as np
import os
import logging
import json
  
from evidently.pipeline.column_mapping import ColumnMapping
 
from evidently.report import Report
from evidently.metric_preset import DataDrift, NumTargetDrift
 
from evidently.test_suite import TestSuite
from evidently.test_preset import DataQuality, DataStability
from evidently.tests import *

f = open(os.path.join("datasets", "params.json"))
params = json.load(f)

def setup_logger():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler()]
    )

def setup_datasets():
    logging.info("Setup datasets.")
    # TODO set the right data input to model
    reference = pd.read_csv(os.path.join("datasets", params["file_name_training_data_clean"]))
    reference.rename(columns={'Quality': 'target'}, inplace=True)
    #reference.rename(columns={'Quality': 'target'}, inplace=True)
    #reference['prediction'] = reference['target'].values + np.random.normal(0, 5, reference.shape[0])

    # TODO set the right input data
    #data_input = [{"Distance (km)": 26.91, "Average Speed (km/h)": 11.08, "Calories Burned": 1266, "Climb (m)": 98, "Average Heart rate (tpm)":121, 'target':5}, {"Distance (km)": 25.91, "Average Speed (km/h)": 14.08, "Calories Burned": 1276, "Climb (m)": 94, "Average Heart rate (tpm)":126, 'target':6}]
    #current = pd.read_csv(os.path.join("datasets", "current.csv"))    ATTENZIONE!!!
    #current = pd.read_csv(os.path.join("datasets", "request_data_clean.csv"))
    current = pd.read_csv(os.path.join("datasets", "current.csv"))
    current.rename(columns={'Quality': 'target'}, inplace=True)
    #print(current['target'])

    # TODO the right output
    #current['prediction'] = math.trunc(5.138380653546847)
    return reference, current

def data_stability_test(reference: pd.DataFrame, current: pd.DataFrame):
    logging.info("Data stability test. Test suite.")
    # A test suite contains several individual tests. Each test compares a specific metric against a defined condition and returns a pass/fail result. 
    # DataStability run several checks for data quality and integrity

    data_stability = TestSuite(tests=[DataStability(),])
    data_stability.run(reference_data=reference, current_data=current)
    data_stability.save_html(os.path.join("metrics_app", "templates", "data_stability.html"))
    #data_stability.save_json("dashboards/data_stability.json")

def drift_report(reference: pd.DataFrame, current: pd.DataFrame):
    logging.info("DataDrift and NumTargetDrift. Drift report.")
    # Reports calculate various metrics and generate a dashboard with rich visuals.

    drift_report = Report(metrics=[DataDrift(), NumTargetDrift()])
    drift_report.run(reference_data=reference, current_data=current)
    drift_report.save_html(os.path.join("metrics_app", "templates", "drift_report.html"))
    #drift_report.save_json("dashboards/drift_report.json")

def data_tests(reference: pd.DataFrame, current: pd.DataFrame):
    logging.info("DataDrift and NumTargetDrift. Drift report.")
    # Data drift and feature drift

    data_drift_tests = TestSuite(tests=[
        TestNumberOfColumnsWithNulls(),
        TestNumberOfRowsWithNulls(),
        TestNumberOfConstantColumns(),
        TestNumberOfDuplicatedRows(),
        TestNumberOfDuplicatedColumns(),
        TestNumberOfDriftedFeatures(),
        TestShareOfDriftedFeatures(),
    ])
    data_drift_tests.run(reference_data=reference, current_data=current)
    data_drift_tests.save_html(os.path.join("metrics_app", "templates", "data_drift_tests.html"))
    #data_drift_tests.save_json("dashboards/data_drift_tests.json")

def main():
    reference, current = setup_datasets()
    data_stability_test(reference, current)
    drift_report(reference, current)
    data_tests(reference, current)

if __name__ == "__main__":    
    main()