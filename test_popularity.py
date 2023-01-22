import pandas as pd
from collections import OrderedDict

import unittest

from popularity_analyzer import PopularityAnalyzer


class TestPopularity(unittest.TestCase):

    def test_get_df_without_top3_popular_objects(self):
        # test that verifies that the get_df_without_top3_popular_objects function returns the dataframe when it does
        # not contain any of the top 3 object names
        df_test = pd.DataFrame({'file_name': ['image1_berlin.txt', 'image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_berlin.txt', 'image2_bonn.txt'],
                                'object_name': ['dog', 'dog', 'dog', 'dog', 'lion']})

        popularity_analyzer = PopularityAnalyzer()
        results_from_df_test = popularity_analyzer.get_df_without_top3_popular_objects(df_test)
        expected_df = pd.DataFrame({'index': 0,
                                    'file_name': ['image1_berlin.txt'],
                                    'object_name': ['dog'],
                                    'count': [4]})
        self.assertTrue(results_from_df_test.equals(expected_df))

    def test_get_df_without_top3_popular_objects_with_popular_object(self):
        # test that verifies that the get_df_without_top3_popular_objects function returns an empty list when the
        # dataframe contain one or various of the top 3 object names
        df_test = pd.DataFrame({'file_name': ['image1_berlin.txt', 'image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_berlin.txt'],
                                'object_name': ['car', 'dog', 'dog', 'dog']})

        popularity_analyzer = PopularityAnalyzer()
        results_from_df_test = popularity_analyzer.get_df_without_top3_popular_objects(df_test)
        expected_df = []
        self.assertEqual(results_from_df_test, expected_df)

    def test_get_popularity_of_objects_under_3(self):
        # test that verifies that the get_popularity_of_objects function returns a popularity ordered dictionary
        # of 3 keys when the dataframe contain three different object_names repeatedly but each with a different repeat
        # number
        df_test = pd.DataFrame({'file_name': ['image1_berlin.txt', 'image2_berlin.txt', 'image3_berlin.txt',
                                              'image3_berlin.txt', 'image1_bonn.txt', 'image2_bonn.txt'],
                                'object_name': ['dog', 'dog', 'dog', 'cat', 'cat', 'lion']})

        popularity_analyzer = PopularityAnalyzer()
        results_from_df_test = popularity_analyzer.get_popularity_of_objects(df_test)
        expected_popularity_dict = OrderedDict([('dog', 3), ('cat', 2), ('lion', 1)])
        self.assertEqual(expected_popularity_dict, results_from_df_test)

    def test_get_popularity_of_objects_above_3_equal_count(self):
        # test that verifies that the get_popularity_of_objects function returns a popularity ordered dictionary
        # of more than 3 keys when the dataframe contain more than 3 different object_names repeatedly but each one with
        # the same repeat number
        df_test = pd.DataFrame({'file_name': ['image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_berlin.txt', 'image1_berlin.txt'],
                                'object_name': ['dog', 'person', 'cat', 'lion']})

        popularity_analyzer = PopularityAnalyzer()
        results_from_df_test = popularity_analyzer.get_popularity_of_objects(df_test)
        expected_popularity_dict = OrderedDict([('cat', 1), ('dog', 1), ('lion', 1), ('person', 1)])
        self.assertEqual(expected_popularity_dict, results_from_df_test)

    def test_get_popularity_of_objects_above_3_different_first_one(self):
        # test that verifies that the get_popularity_of_objects function returns a popularity ordered dictionary
        # of 1 keys when the dataframe contain more than 3 different object_names repeatedly but each one have the same
        # repeat number except one that have a higher number
        df_test = pd.DataFrame({'file_name': ['image1_berlin.txt', 'image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_berlin.txt', 'image1_berlin.txt'],
                                'object_name': ['dog', 'dog', 'cat', 'lion', 'giraffe']})

        popularity_analyzer = PopularityAnalyzer()
        results_from_df_test = popularity_analyzer.get_popularity_of_objects(df_test)
        expected_popularity_dict = OrderedDict([('dog', 1)])
        self.assertEqual(expected_popularity_dict, results_from_df_test)

    def test_get_popularity_of_objects_above_3_different_first_and_second_one(self):
        # test that verifies that the get_popularity_of_objects function returns a popularity ordered dictionary
        # of 2 keys when the dataframe contain more than 3 different object_names repeatedly but each one have the same
        # repeat number except the first and second one that have a higher different number.
        df_test = pd.DataFrame({'file_name': ['image1_berlin.txt', 'image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_berlin.txt', 'image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_berlin.txt'],
                                'object_name': ['dog', 'dog', 'dog', 'cat', 'cat', 'lion', 'giraffe']})

        popularity_analyzer = PopularityAnalyzer()
        results_from_df_test = popularity_analyzer.get_popularity_of_objects(df_test)
        expected_popularity_dict = OrderedDict([('dog', 1), ('cat', 1)])
        self.assertEqual(expected_popularity_dict, results_from_df_test)

    def test_get_popularity_of_objects_above_3_first_and_second_one_same_count(self):
        # test that verifies that the get_popularity_of_objects function returns a popularity ordered dictionary
        # of 2 keys when the dataframe contain more than 3 different object_names repeatedly but each one have the same
        # repeat number except the first and second one that have the same higher number.
        df_test = pd.DataFrame({'file_name': ['image1_berlin.txt', 'image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_berlin.txt', 'image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_berlin.txt'],
                                'object_name': ['dog', 'dog', 'cat', 'cat', 'lion', 'snowman', 'giraffe']})

        popularity_analyzer = PopularityAnalyzer()
        results_from_df_test = popularity_analyzer.get_popularity_of_objects(df_test)
        expected_popularity_dict = OrderedDict([('cat', 1), ('dog', 1)])
        self.assertEqual(expected_popularity_dict, results_from_df_test)

    def test_get_popularity_of_objects_above_3_the_first_three_ones_have_different_counts(self):
        # test that verifies that the get_popularity_of_objects function returns a popularity ordered dictionary
        # of 3 keys when the dataframe contain more than 3 different object_names repeatedly but each one have the same
        # repeat number except the first, second and third one that have a higher different number.
        df_test = pd.DataFrame({'file_name': ['image1_berlin.txt', 'image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_berlin.txt', 'image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_berlin.txt', 'image1_berlin.txt', 'image1_berlin.txt',
                                              'image1_berlin.txt'],
                                'object_name': ['dog', 'dog', 'dog', 'dog', 'cat', 'cat', 'cat', 'lion', 'lion',
                                                'person']})

        popularity_analyzer = PopularityAnalyzer()
        results_from_df_test = popularity_analyzer.get_popularity_of_objects(df_test)
        expected_popularity_dict = OrderedDict([('dog', 1), ('cat', 1), ('lion', 1)])
        self.assertEqual(expected_popularity_dict, results_from_df_test)


unittest.main(argv=['first-arg-is-ignored'], verbosity=2, exit=False)
