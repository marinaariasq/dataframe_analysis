class Processor:

    def get_first_image_by_city_file_name(self, df):
        """
        This function returns the file path of the first image for each unique city in the given dataframe (df).

        Inputs:
        df: [pandas dataframe] original dataframe containing the data

        Outputs:
        first_images_by_city_file_paths: [list] list containing the file path of the first image for each unique
        city in the dataframe.
        """

        # obtain each city mentioned in the data frame
        city_names = df['city_name'].unique()

        first_images_by_city_file_paths = []

        for name in city_names:
            rows = df.loc[df['city_name'] == name]
            first_file_path = rows.loc[:, 'file_name'].iloc[0]
            first_images_by_city_file_paths.append(first_file_path)
        return first_images_by_city_file_paths

    def get_image_objects_by_file_name(self, df, label_name):
        """
        This function returns the rows from the given dataframe (df) that have the specified label_name.

        Inputs:
        df: [pandas dataframe] original dataframe containing the data
        label_name: [string] name of the file to search for in the 'file_name' column of the dataframe

        Outputs:
        df: [pandas dataframe] dataframe containing the rows from the original dataframe with the specified
        label_name
        """
        return df.loc[df['file_name'] == label_name]

    def filter_dataframe_by_high_yolo(self, df):
        """
        This function filters the given dataframe (df) by removing all rows where the 'YOLO_prob' column is less than or
        equal to 0.4

        Inputs:
        df: [pandas dataframe] original dataframe containing the data

        Outputs:
        df: [pandas dataframe] dataframe containing only the rows where the 'YOLO_prob' column is greater than 0.4 from
        the original dataframe
        """
        df['YOLO_prob'] = df['YOLO_prob'].astype(float)
        return df.loc[df['YOLO_prob'] > 0.4]

    def get_object_id_count_of_dataframe(self, df):
        """
        This function returns the count of each unique object_id and object_name combination in the given dataframe (df)
        sorted by count in descending order.

        Inputs:
        df: [pandas dataframe] original dataframe containing the data

        Outputs:
        df: [pandas dataframe] dataframe containing columns 'object_id', 'object_name' and 'count' where count is the
        number of times each unique combination of object_id and object_name appears in the original dataframe.
        """
        return df.groupby(['object_id', 'object_name']).size().sort_values(ascending=False).reset_index(name='count')

    def get_objectname_count_by_file(self, df):
        """
        This function returns the count of each unique object_name by file_name in the given dataframe (df).

        Inputs:
        df: [pandas dataframe] original dataframe containing the data

        Outputs:
        df: [pandas dataframe]  dataframe containing columns 'file_name', 'object_name' and 'count' where count is the
        number of times each unique object_name appears in the file_name from the original dataframe
        """
        return df.groupby(['file_name', 'object_name']).size().reset_index(name='count')

    def average_number_objects_by_file(self, df):
        """
        This function returns the average number of objects in the given dataframe (df) grouped by file_name.

        Inputs:
        df: [pandas dataframe] original dataframe containing the data

        Outputs:
        average_total_objects_by_image: [int] the average number of objects by file_name.
        """
        total_objects_by_file = df.groupby(['file_name']).size().reset_index(name='count')
        average_total_objects_by_image = total_objects_by_file["count"].mean().astype(int)
        return average_total_objects_by_image

    def insert_city_year_to_df(self, df):
        """
        This function adds new columns "city" and "year" to the given data frame (df).
        The "city" and "year" information is extracted from the "file_name" column.
            Where the string 'city' is the first part of the string from 'file_name' before the first '_'.
            Where the string 'year' is the 4digits part of the string from 'file_name' before the last '.'.

        Inputs:
        df: [pandas dataframe] original dataframe containing the data

        Outputs:
        df: [pandas dataframe] containing the original dataframe with new columns 'city' and 'year'
        """
        df['city'] = df['file_name'].str.extract(r'^([a-z]+)')
        df['year'] = df['file_name'].str.extract(r'(\d{4}).txt$')
        return df
