# mu-value-peak-detect (Cloud Function)
This code detects value peak from MU datasets to be analyzed.
This is a Cloud Function that search peak Volum values of Measurement Units (negative delta values coming from the substraction of the current value and the previous of the same MU and line).

## Overview
This tool gets a list of UM's and a range dates and looks for negative delta values. This will return a list of rows containing all dataset values inclufding the delta with negative value in the Cloud Function log.


## How to run

- Go to [Google Cloud Console](https://cloud.google.com/).
- Select `SEA Produccion`project.
- Select `CLoud Functions`service.
- Select `mu_peak_detector` cloud function from the list.
- Select `TESTING` tab.
- Insert input parameters:
  - `list_mu_id`: List of Measurement Unit ID's
  - `date_range_start`: The start date of a range of dates.
  - `date_range_end`: The end date of a range of dates.
  - JSON Input format:
    ```
    {
        "list_mu_id": [
            "mu_id_1",
            "mu_id_2",
            ...
            "mu_id_n"
        ],
        "date_range": {
            "start": "YYYY-MM-DD",
            "end": "YYYY-MM-DD"
        }
    }
    ```
    - Example:
        ```
        {
            "list_mu": [
                "9c140b4d-04fe-4053-a573-e26d5a2a2f5a"
            ],
            "date_range": {
                "start": "2021-01-01",
                "end": "2023-05-26"
            }
        }
        ```
  - Wait and check the results at `LOGS`.
