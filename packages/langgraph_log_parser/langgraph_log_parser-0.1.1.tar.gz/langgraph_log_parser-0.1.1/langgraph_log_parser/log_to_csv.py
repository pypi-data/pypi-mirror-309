import os
import json
import csv


def export_logs_to_csv(
        logs_folder='files/logs',
        csv_path='files/combined_output.csv',
        csv_fields=None,
        exclude_activities=None,
        resource_mapping=None
):
    """
    Convert multiple JSON log files in a folder to a single aggregated CSV file,
    filtering out rows with specified activities.

    :param logs_folder: Path to the folder containing JSON log files.
    :type logs_folder: str
    :param csv_path: Path to the output aggregated CSV file.
    :type csv_path: str
    :param csv_fields: List of field names for the CSV file. Default fields are:
                       ['case_id', 'timestamp', 'end_timestamp', 'cost', 'activity', 'org:resource'].
    :type csv_fields: list[str], optional
    :param exclude_activities: List of activities to exclude from the final CSV file.
    :type exclude_activities: list[str], optional
    :param resource_mapping: Mapping of `writes` values to `org:resource` values.
    :type resource_mapping: dict[str, str], optional
    """
    if csv_fields is None:
        csv_fields = ['case_id', 'timestamp', 'end_timestamp', 'cost', 'activity', 'org:resource']

    if exclude_activities is None:
        exclude_activities = []

    if resource_mapping is None:
        resource_mapping = {}

    # Ensure output folder exists
    output_folder = os.path.dirname(csv_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize the aggregated CSV file with headers
    with open(csv_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
        writer.writeheader()

    # Process each log file in the folder
    last_org_resource = None  # Store the last resource from the mapping
    for log_file_name in os.listdir(logs_folder):
        log_file_path = os.path.join(logs_folder, log_file_name)
        if not log_file_name.endswith('.log'):
            # Skip files that are not .log
            continue

        # Read data from JSON log file
        with open(log_file_path, 'r') as log_file:
            logs = json.load(log_file)

        # Append processed data to the aggregated CSV file
        with open(csv_path, mode='a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_fields)

            for i, log_entry in enumerate(logs):
                case_id = log_entry.get('thread_ID')
                timestamp = log_entry['checkpoint'].get('ts')
                cost = 0

                metadata = log_entry.get('metadata', {})
                writes = metadata.get('writes', {})

                if writes and isinstance(writes, dict):
                    activity = list(writes.keys())[0]
                    org_resource = resource_mapping.get(activity, last_org_resource)  # Use mapped or last value
                    last_org_resource = org_resource  # Update the last org_resource
                else:
                    continue  # Skip entries without `writes`

                # Skip rows with excluded activities
                if activity in exclude_activities:
                    continue

                end_timestamp = None
                for j in range(i + 1, len(logs)):
                    next_log_entry = logs[j]
                    if next_log_entry.get('thread_ID') == case_id:
                        if next_log_entry.get('metadata', {}).get('writes'):
                            end_timestamp = next_log_entry['checkpoint'].get('ts')
                            break

                writer.writerow({
                    'case_id': case_id,
                    'timestamp': timestamp,
                    'end_timestamp': end_timestamp if end_timestamp is not None else timestamp,
                    'cost': cost,
                    'activity': activity,
                    'org:resource': org_resource
                })
