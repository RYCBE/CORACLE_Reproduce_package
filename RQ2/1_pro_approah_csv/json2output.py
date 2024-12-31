import csv
import json


def process_data_to_csv_format(data):
    """
    Process the input data into a format suitable for writing to a CSV file (each line: project, version, method tags)
    """
    result_rows = []
    for project, project_versions in data.items():
        for version, method_results in project_versions.items():
            row = [project, version] + method_results
            result_rows.append(row)
    return result_rows


if __name__ == "__main__":
    with open("no_issue_code_av.json", "r") as f:
        data = json.load(f)

    csv_data = process_data_to_csv_format(data)
    header = ["project", "version"] + [
        'Simple',
        'Proportion_ColdStart',
        'Proportion_Increment',
        'Proportion_MovingWindow',
        'SZZ_U',
        'SZZ_B',
        'SZZ_RA',
        'Proportion_ColdStart+',
        'Proportion_Increment+',
        'Proportion_MovingWindow+',
        'SZZ_U+',
        'SZZ_B+',
        'SZZ_RA+',
        'Actual',
        'CORACLE',
    ]

    with open("output.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(csv_data)
