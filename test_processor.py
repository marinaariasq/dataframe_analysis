import unittest
import pandas as pd

from processor import Processor


class TestProcessor(unittest.TestCase):

    def test_get_first_image_by_city_file_name(self):
        # test that verifies that the get_first_image_by_city_file_name function returns a list of the first file name
        # for each city.
        df_test = pd.DataFrame({'city_name': ['berlin', 'berlin', 'zurich', 'bonn', 'zurich', 'bonn'],
                                'file_name': ['image1_berlin.txt', 'image2_berlin.txt', 'image1_zurich.txt',
                                              'image1_bonn.txt', 'image2_zurich.txt', 'image2_bonn.txt']})

        processor = Processor()
        result_from_df_test = processor.get_first_image_by_city_file_name(df_test)
        list_first_images_by_city_expected = ['image1_berlin.txt', 'image1_zurich.txt', 'image1_bonn.txt']
        self.assertEqual(result_from_df_test, list_first_images_by_city_expected)

    def test_get_image_objects_by_file_name(self):
        # test that verifies that the get_image_objects_by_file_name function returns a dataframe of the object_names
        # in a specific file_name.
        df_test = pd.DataFrame({'file_name': ['image1_berlin.txt', 'image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_bonn.txt', 'image1_bonn.txt', 'image2_bonn.txt'],
                                'object_name': ['car', 'person', 'traffic light', 'person', 'car', 'car']})

        label_file_name_to_detect = 'image1_berlin.txt'

        processor = Processor()
        result_from_df_test = processor.get_image_objects_by_file_name(df_test, label_file_name_to_detect)
        df_specific_file_expected = pd.DataFrame(
            {'file_name': ['image1_berlin.txt', 'image1_berlin.txt', 'image1_berlin.txt'],
             'object_name': ['car', 'person', 'traffic light']})
        self.assertTrue(result_from_df_test.equals(df_specific_file_expected))

        processor = Processor()
        result_from_df_test = processor.get_image_objects_by_file_name(df_test, label_file_name_to_detect)
        df_specific_file_not_expected = pd.DataFrame({'file_name': ['image1_bonn.txt', 'image1_bonn.txt'],
                                                      'object_name': ['person', 'car']})
        self.assertFalse(result_from_df_test.equals(df_specific_file_not_expected))

    def test_filter_dataframe_by_high_yolo_in_dataframe_with_high_yolo(self):
        # test that verifies that the filter_dataframe_by_high_yolo function returns a dataframe with a higher YOLO
        # probability
        df_test = pd.DataFrame({'YOLO_prob': ['0.55', '0.68', '0.88'],
                                'object_name': ['car', 'person', 'traffic light']})

        processor = Processor()
        result_from_df_test = processor.filter_dataframe_by_high_yolo(df_test)
        expected_results_object_id = pd.DataFrame({'YOLO_prob': [0.55, 0.68, 0.88],
                                                   'object_name': ['car', 'person', 'traffic light']})

        self.assertTrue(result_from_df_test.equals(expected_results_object_id))

    def test_filter_dataframe_by_high_yolo_in_dataframe_with_low_yolo(self):
        # test that verifies that the filter_dataframe_by_high_yolo function does not return de dataframe with a
        # low YOLO probability
        df_test2 = pd.DataFrame({'YOLO_prob': ['0.33', '0.28', '0.18'],
                                 'object_name': ['car', 'person', 'traffic light']})
        processor = Processor()
        result_from_df_test = processor.filter_dataframe_by_high_yolo(df_test2)
        expected_results_object_id = pd.DataFrame({'YOLO_prob': [0.33, 0.28, 0.18],
                                                   'object_name': ['car', 'person', 'traffic light']})
        self.assertFalse(result_from_df_test.equals(expected_results_object_id))

    def test_get_object_id_count_of_dataframe(self):
        # test that verifies that the get_object_id_count_of_dataframe function returns de dataframe with the
        # object_name and object_id count
        df_test = pd.DataFrame({'object_id': [1, 2, 2, 3, 3],
                                'object_name': ['car', 'person', 'person', 'traffic', 'traffic']})

        processor = Processor()
        result_object_id_count = processor.get_object_id_count_of_dataframe(df_test)
        expected_results_object_id = pd.DataFrame({'object_id': [2, 3, 1],
                                                   'object_name': ['person', 'traffic', 'car'],
                                                   'count': [2, 2, 1]})
        self.assertTrue(result_object_id_count.equals(expected_results_object_id))

        df_test = pd.DataFrame({'object_id': [1, 1, 2, 3, 3],
                                'object_name': ['car', 'car', 'person', 'traffic', 'traffic']})
        result_object_id_count = processor.get_object_id_count_of_dataframe(df_test)
        unexpected_results_object_id = pd.DataFrame({'object_id': [2, 3, 1],
                                                     'object_name': ['person', 'traffic', 'car'],
                                                     'count': [2, 2, 1]})
        self.assertFalse(result_object_id_count.equals(unexpected_results_object_id))

    def test_get_objectname_count_by_file(self):
        # test that verifies that the get_object_id_count_of_dataframe function returns de dataframe with the
        # object_name count for each file_name
        df_test = pd.DataFrame({'file_name': ['image1_berlin.txt', 'image1_bonn.txt', 'image1_berlin.txt',
                                              'image1_bonn.txt', 'image1_bonn.txt'],
                                'object_name': ['car', 'person', 'person', 'traffic', 'traffic']})

        processor = Processor()
        result_object_id_count = processor.get_objectname_count_by_file(df_test)
        expected_results_object_id = pd.DataFrame(
            {'file_name': ['image1_berlin.txt', 'image1_berlin.txt', 'image1_bonn.txt',
                           'image1_bonn.txt'],
             'object_name': ['car', 'person', 'person', 'traffic'],
             'count': [1, 1, 1, 2]})
        self.assertTrue(result_object_id_count.equals(expected_results_object_id))

    def test_average_number_objects_by_file(self):
        # test that verifies that the average_number_objects_by_file function returns the average object_id count for
        # each file of a given dataframe
        df_test = pd.DataFrame({'file_name': ['image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_bonn.txt', 'image1_bonn.txt'],
                                'object_name': ['car', 'person', 'person', 'traffic', 'person', 'traffic']})

        processor = Processor()
        result_average_count_object_id_by_file = processor.average_number_objects_by_file(df_test)
        average_total_object_expected = 3
        self.assertTrue(result_average_count_object_id_by_file == average_total_object_expected)

    def test_insert_city_year_to_df(self):
        # test that verifies that the insert_city_year_to_df function inserts 'city' and 'year' columns with their
        # corresponding values for a given dataframe
        df_test = pd.DataFrame({'file_name': ['berlin_2021.txt', 'berlin_2022.txt',
                                              'bonn_2020.txt', 'bonn_2019.txt'],
                                'object_name': ['car', 'person', 'person', 'traffic']})
        processor = Processor()
        result_df_amplified = processor.insert_city_year_to_df(df_test)
        expected_df_amplified = pd.DataFrame({'file_name': ['berlin_2021.txt', 'berlin_2022.txt',
                                                            'bonn_2020.txt', 'bonn_2019.txt'],
                                              'object_name': ['car', 'person', 'person', 'traffic'],
                                              'city': ['berlin', 'berlin', 'bonn', 'bonn'],
                                              'year': ['2021', '2022', '2020', '2019']})
        self.assertTrue(result_df_amplified.equals(expected_df_amplified))


# check results from test
unittest.main(argv=['first-arg-is-ignored'], verbosity=2, exit=False)
