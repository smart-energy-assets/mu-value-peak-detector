import pandas as pd
import warnings
from google.cloud import bigquery


# Disable pandas warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)
# Create a BigQuery client
bq_client = bigquery.Client()


def get_data_from_query(dataset_id, start_date, end_date):
    # Construct the SQL query to fetch the data
    sql_query = f"""
        SELECT
            TS,
            Vn,
            muName,
            lName,
            source
        FROM 
            `sea-produccion.gas_data.GasVolumes`
        WHERE
            DATE(TS) BETWEEN "{start_date}" AND "{end_date}"
                    AND muName = "{dataset_id}"
        ORDER BY
            TS asc
    """

    # Run the query and retrieve the results and convert it to pandas's dataframe
    df = bq_client.query(sql_query).to_dataframe()

    return df

def get_negative_deltas(dataset):
    # Calculate the Delta_Vn between the current and previous Vn values
    dataset['Delta_Vn'] = dataset['Vn'].diff().round(2)
    # Filter and print the rows where the 'Delta_Vn' column is negative
    print("\nRows with negative delta Vn:")
    negative_rows = dataset[dataset['Delta_Vn'] < 0]
    if len(negative_rows.index) > 0:
        print(f"Number of peaks: {len(negative_rows.index)}")
        print(negative_rows)
    else:
        print("No")

def get_peaks(df):
    # TS,Vn,muName,lName,source
    # Filter duplicates based on a single column
    # Create separate datasets for each duplicate value in a specific column
    unique_values = df.drop_duplicates(subset='lName')
    datasets = []
    for value in unique_values['lName']:
        dataset = df[df['lName'] == value]
        datasets.append(dataset)

    for index, dataset in enumerate(datasets):
        # Assuming you have a dataset stored in a DataFrame called 'data'
        row_index = 0
        mu_name = df.loc[row_index, 'muName']
        lName = df.loc[row_index, 'lName']
        print(f"\n{'-'*60}\nDataset #{index}:\n - Measurement Unit name: {mu_name}\n - Line name: {lName}\n{'-'*60}")
        get_negative_deltas(dataset)

def main(request):
    print("[INFO] Start peak serach execution")
    # Main execution
    request_json = request.get_json()
    # Parse the JSON input
    list_datasets_id = request_json["list_mu"]
    range_start_date = request_json["date_range"]["start"]
    range_end_date = request_json["date_range"]["end"]
    print(f"[INFO] List of MU's range -> {list_datasets_id}")
    print(f"[INFO] Date range -> From {range_start_date} to {range_end_date}")

    # Start searching fopr peaks in all listed MU's
    for dataset_id in list_datasets_id:
        print(f"[INFO] Query data from MU ID {dataset_id}")
        dataset_data = get_data_from_query(dataset_id, range_start_date, range_end_date)
        print(f"[INFO] get peaks for MU ID {dataset_id} in all its lines ")
        get_peaks(dataset_data)

    print("[INFO] End peak serach execution")
