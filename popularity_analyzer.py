from collections import OrderedDict


class PopularityAnalyzer:

    def __create_ordered_dictionary(self, popularity_matrix):
        """
        This function returns a sorted dictionary from a list of lists. This dictionary will contain as key all the
        types of objects present in the lists of the list and each key will have as value the total number of times
        this object have appeared in the lists.

        Inputs:
        popularity_matrix: [list] list that contains the lists of the most popular object_names for each file_name

        Outputs:
        dict_ordered_popular_objects: [OrderedDict] ordered dictionary of the object_names popularity
        """
        dict_popular_objects = OrderedDict()
        for top_objects in popularity_matrix:
            for object_name in top_objects:
                dict_popular_objects[object_name] = dict_popular_objects.get(object_name, 0) + 1
        dict_ordered_popular_objects = OrderedDict(
            sorted(dict_popular_objects.items(), key=lambda item: item[1], reverse=True))
        return dict_ordered_popular_objects

    def __get_ordered_object_id_count_by_file(self, df):
        """
        This function returns the count of each unique object_name and file_name combination in the given dataframe (df)
        sorted by count in descending order.

        Inputs:
        df: [pandas dataframe] original dataframe containing the data

        Outputs: [tuple] The tuple contains the ordered_df and list_filenames. Where:
                - ordered_df : [pandas dataframe] dataframe containing columns 'object_name', 'object_name' and 'count'
                where count is the number of times each unique combination of object_id and object_name appears in
                the original dataframe.
                - list_filenames : [list] list of each file_name from the ordered_df dataframe
        """
        ordered_df = (df.groupby(['file_name', 'object_name'])).size().reset_index(
            name='count').sort_values(by='count', ascending=False)
        list_filenames = ordered_df['file_name'].unique()
        return ordered_df, list_filenames

    def get_df_without_top3_popular_objects(self, df):
        """
        This function returns a data frame of the first type of file_name that does not contain any of the 3 most
        popular objects of the original data frame.

        Inputs:
        df: [pandas dataframe] original dataframe containing the data

        Outputs:
        df_count_per_file: [pandas dataframe] dataframe of the first file_name without the 3 most popular objects of the
        original dataframe

        """
        df_ordered_object_count_by_image, list_labels = self.__get_ordered_object_id_count_by_file(df)

        for file in list_labels:
            # get rows of specific file_name from dataframe and reset index
            df_count_per_file = df_ordered_object_count_by_image[
                df_ordered_object_count_by_image['file_name'] == file].reset_index()
            # obtain the 3 rows with the highest count value
            df_most_popular_object_names = df_count_per_file.nlargest(3, 'count')
            if not df_most_popular_object_names['object_name'].str.contains('car').any() and \
                    not df_most_popular_object_names['object_name'].str.contains('person').any() and \
                    not df_most_popular_object_names['object_name'].str.contains('traffic light').any():
                return df_count_per_file

        return []

    def get_popularity_of_objects(self, df):
        """
        This function generates an ordered dictionary of object popularity from the original dataframe. It will
        process the dataframe generating a list with the object_names that have been detected more times for each of
        the file_names. Then it will add each of the lists to a main list that will be used to generate the ordered
        dictionary.

        Inputs:
        df: [pandas dataframe] original dataframe containing the data

        Outputs:
        ordered_popularity_object_dictionary: [OrderedDict] ordered dictionary of the object_names popularity

        """

        df_ordered_object_count_by_image, list_file_labels = self.__get_ordered_object_id_count_by_file(df)
        matrix_total_top3_per_image = []

        for file in list_file_labels:
            df_count_per_file = df_ordered_object_count_by_image[
                df_ordered_object_count_by_image['file_name'] == file].reset_index()

            # check how many rows have the dataframe of the specific file_name
            total_object_count = df_count_per_file.shape[0]
            # total_object_count under or equal to 3 or total_object_count above 3 but each object name have the same
            # count, preserve the reduced dataframe as the dataframe with the most popular object_names
            df_most_popular_object_names = df_count_per_file

            # if total_object_count above 3 and different counts each object_name
            if total_object_count > 3 and df_count_per_file['count'].nunique() != 1:
                top1_object_count = df_count_per_file['count'].iloc[0]
                top2_object_count = df_count_per_file['count'].iloc[1]
                top3_object_count = df_count_per_file['count'].iloc[2]
                top4_object_count = df_count_per_file['count'].iloc[3]

                # the first object_name have more counts thant the others, and the others have the same number of
                # counts
                if top1_object_count != top2_object_count and \
                        top2_object_count == top3_object_count and \
                        top3_object_count == top4_object_count:

                    df_most_popular_object_names = df_count_per_file.nlargest(1, 'count')

                # the first and second object_name have more counts thant the others, and the others have the same
                # number of  counts
                elif (top1_object_count != top2_object_count or top1_object_count == top2_object_count) and \
                        top2_object_count != top3_object_count and \
                        top3_object_count == top4_object_count:

                    df_most_popular_object_names = df_count_per_file.nlargest(2, 'count')

                # the first, the second and the third object_name have more counts thant the others
                elif top1_object_count != top2_object_count and \
                        top2_object_count != top3_object_count and \
                        top3_object_count != top4_object_count:

                    df_most_popular_object_names = df_count_per_file.nlargest(3, 'count')

            # add the row object_name of the dataframe containing the most popular object_names as a list into the main
            # list
            matrix_total_top3_per_image.append(df_most_popular_object_names['object_name'].tolist())

        ordered_popularity_object_dictionary = self.__create_ordered_dictionary(matrix_total_top3_per_image)

        return ordered_popularity_object_dictionary
