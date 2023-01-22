from collections import OrderedDict


class PopularityAnalyzer:

    def __create_ordered_dictionary(self, popularity_matrix):
        dict_popular_objects = OrderedDict()
        for top_objects in popularity_matrix:
            for object_name in top_objects:
                dict_popular_objects[object_name] = dict_popular_objects.get(object_name, 0) + 1
        dict_ordered_popular_objects = OrderedDict(
            sorted(dict_popular_objects.items(), key=lambda item: item[1], reverse=True))
        return dict_ordered_popular_objects

    def __get_ordered_object_id_count_by_file(self, df):
        ordered_df = (df.groupby(['file_name', 'object_name'])).size().reset_index(
            name='count').sort_values(by='count', ascending=False)
        list_filenames = ordered_df['file_name'].unique()
        return ordered_df, list_filenames

    def get_df_without_top3_popular_objects(self, df):
        df_ordered_object_count_by_image, list_file_labels = self.__get_ordered_object_id_count_by_file(df)

        for file in list_file_labels:
            df_count_per_file = df_ordered_object_count_by_image[
                df_ordered_object_count_by_image['file_name'] == file].reset_index()
            df_most_popular_object_names = df_count_per_file.nlargest(3, 'count')
            if not df_most_popular_object_names['object_name'].str.contains('car').any() and \
                    not df_most_popular_object_names['object_name'].str.contains('person').any() and \
                    not df_most_popular_object_names['object_name'].str.contains('traffic light').any():
                return df_count_per_file

        return []

    def get_popularity_of_objects(self, df):

        df_ordered_object_count_by_image, list_file_labels = self.__get_ordered_object_id_count_by_file(df)
        matrix_total_top3_per_image = []

        for file in list_file_labels:
            df_count_per_file = df_ordered_object_count_by_image[
                df_ordered_object_count_by_image['file_name'] == file].reset_index()
            total_object_count = df_count_per_file.shape[0]

            df_most_popular_object_names = df_count_per_file
            if total_object_count > 3 and df_count_per_file['count'].nunique() != 1:
                top1_object_count = df_count_per_file['count'].iloc[0]
                top2_object_count = df_count_per_file['count'].iloc[1]
                top3_object_count = df_count_per_file['count'].iloc[2]
                top4_object_count = df_count_per_file['count'].iloc[3]

                if top1_object_count != top2_object_count and \
                        top2_object_count == top3_object_count and \
                        top3_object_count == top4_object_count:

                    df_most_popular_object_names = df_count_per_file.nlargest(1, 'count')

                elif (top1_object_count != top2_object_count or top1_object_count == top2_object_count) and \
                        top2_object_count != top3_object_count and \
                        top3_object_count == top4_object_count:

                    df_most_popular_object_names = df_count_per_file.nlargest(2, 'count')

                elif top1_object_count != top2_object_count and \
                        top2_object_count != top3_object_count and \
                        top3_object_count != top4_object_count:

                    df_most_popular_object_names = df_count_per_file.nlargest(3, 'count')

            matrix_total_top3_per_image.append(df_most_popular_object_names['object_name'].tolist())

        ordered_popularity_object_dictionary = self.__create_ordered_dictionary(matrix_total_top3_per_image)

        return ordered_popularity_object_dictionary
