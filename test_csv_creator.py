import pandas as pd
import os
import csv
import re
import unittest

from csv_creator import CsvCreator


class TestCsvCreator(unittest.TestCase):
    def test_create_csv_file_from_df(self):
        df_test = pd.DataFrame({'file_name': ['berlin_2020.txt', 'berlin_2020.txt', 'berlin_2020.txt',
                                              'bonn_2022.txt', 'bonn_2022.txt', 'bonn_2022.txt'],
                                'object_name': ['car', 'person', 'dog', 'person', 'person', 'car'],
                                'Image_type': ['Intrusive image', 'Intrusive image', 'Intrusive image',
                                               'City_image', 'City_image', 'City_image']})

        csv_creator = CsvCreator()
        test_name = 'images_test.csv'
        test_csv_name, path_test_csv = csv_creator.create_csv_file_from_df(df_test, test_name)
        self.assertEqual(test_csv_name, test_name)
        self.assertTrue(os.path.isfile(path_test_csv))


unittest.main(argv=['first-arg-is-ignored'], verbosity=2, exit=False)
