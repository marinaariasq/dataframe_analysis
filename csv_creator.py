import os
import csv
import re

IMAGE_FILE_FORMAT = '.png'


class CsvCreator:

    def create_csv_file_from_df(self, df, file_name):
        """
        This function creates a CSV file from the given dataframe (df) and saves it to the local directory. The name of
        the file is passed as an argument (file_name).

        Inputs:
        df: [pandas dataframe] original dataframe containing the data
        file_name: [string] name of the CSV file to be created

        Outputs: [tuple] The tuple contains the csv_file_name and csv_file_path. Where
                - csv_file_name : [string] name of the created CSV file.
                - csv_file_path : [string] absolute path of the created CSV file.
        """

        label_names = df['file_name'].tolist()
        label_names_without_duplicates = list(set(label_names))
        csv_file_name = file_name
        file_exists = os.path.isfile(csv_file_name)
        with open(csv_file_name, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            if not file_exists:
                csvwriter.writerow(
                    ['image_name', 'car_count', 'traffic_lights_count', 'persons_count', 'city', 'year', 'image_type'])

            for file in label_names_without_duplicates:
                df_specific_file = df[df['file_name'] == file].reset_index()
                image_name = file.replace(".txt", IMAGE_FILE_FORMAT)
                city_name = file.split('_')[0]
                match_year = re.search(r'(\d{4}).txt$', file)
                year = match_year.group(1)
                image_type = df_specific_file['Image_type'].iloc[0]
                car_count = df_specific_file['object_name'].str.count('car').sum()
                person_count = df_specific_file['object_name'].str.count('person').sum()
                trafficlight_count = df_specific_file['object_name'].str.count('traffic light').sum()
                row = [image_name, car_count, trafficlight_count, person_count, city_name, year, image_type]
                csvwriter.writerow(row)

            return csv_file_name, os.path.abspath(csv_file_name)
