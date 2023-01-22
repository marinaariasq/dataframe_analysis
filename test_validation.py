import unittest
import csv
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from validation import Validation

test_check_yolo_file_path = '/home/datasci/PycharmProjects/pac4/test_check_yolo.csv'


class TestValidation(unittest.TestCase):

    def test_check_yolo_valid(self):
        # test that verifies that the check_yolo function returns a True when the dataframe complies with the yolo
        # format
        with open(test_check_yolo_file_path, 'w') as file:
            csv_writer = csv.writer(file, delimiter=' ')
            csv_writer.writerow(['0', '0.22', '0.44', '0.32', '0.49', '0.511'])
            csv_writer.writerow(['4', '0.77', '0.23', '0.99', '0.38', '0.67'])

        self.assertEqual(Validation.check_yolo(test_check_yolo_file_path), True)

    def test_check_yolo_missing_columns(self):
        # test that verifies that the check_yolo function returns a False when the dataframe does not meet with the
        # yolo format because it is missing columns
        with open(test_check_yolo_file_path, 'w') as file:
            csv_writer = csv.writer(file, delimiter=' ')
            csv_writer.writerow(['0', '0.22', '0.44', '0.32'])
        self.assertEqual(Validation.check_yolo(test_check_yolo_file_path), False)

    def test_check_yolo_wrong_number_column_value(self):
        # test that verifies that the check_yolo function returns a False when the dataframe does not meet with the
        # yolo format because the coordinates values are not between 0 and 1
        with open(test_check_yolo_file_path, 'w') as file:
            csv_writer = csv.writer(file, delimiter=' ')
            csv_writer.writerow(['0', '0.22', '0.44', '4', '0.49', '0.511'])
        self.assertEqual(Validation.check_yolo(test_check_yolo_file_path), False)

    def test_check_yolo_wrong_number_column_type(self):
        # test that verifies that the check_yolo function returns a False when the dataframe does not meet with the
        # yolo format because the coordinates values are not an int
        with open(test_check_yolo_file_path, 'w') as file:
            csv_writer = csv.writer(file, delimiter=' ')
            csv_writer.writerow(['0', '0.22', '0.44', 'wrongType', '0.49', '0.511'])
        self.assertEqual(Validation.check_yolo(test_check_yolo_file_path), False)

    def test_check_yolo_wrong_id_column_value(self):
        # test that verifies that the check_yolo function returns a False when the dataframe does not meet with the
        # yolo format because the object_id values are not between 0 and 80
        with open(test_check_yolo_file_path, 'w') as file:
            csv_writer = csv.writer(file, delimiter=' ')
            csv_writer.writerow(['99', '0.22', '0.44', '0.32', '0.49', '0.511'])
        self.assertEqual(Validation.check_yolo(test_check_yolo_file_path), False)

    def test_check_yolo_wrong_id_column_type(self):
        # test that verifies that the check_yolo function returns a False when the dataframe does not meet with the
        # yolo format because the object_id values are not an int
        with open(test_check_yolo_file_path, 'w') as file:
            csv_writer = csv.writer(file, delimiter=' ')
            csv_writer.writerow(['x9', '0.22', '0.44', '0.32', '0.49', '0.511'])
        self.assertEqual(Validation.check_yolo(test_check_yolo_file_path), False)

    def test_check_intrusive_images_non_intrusive(self):
        # test that verifies that the test_check_intrusive_images_non_intrusive function returns a True when the
        # image have the metadata corresponding to a City Image
        img = Image.new('RGB', (30, 30), color='red')
        # A PngInfo must be created to add the metadata to the .PNG file (otherwise the metadata will not be
        # inserted into the image when it is saved).
        meta = PngInfo()
        meta.add_text("Gamma", "444")
        image_path = '/home/datasci/PycharmProjects/pac4/test_img_city.png'
        img.save(image_path, "PNG", pnginfo=meta)

        self.assertEqual(Validation.check_intrusive_images(image_path), True)

    def test_check_intrusive_images_intrusive(self):
        # test that verifies that the test_check_intrusive_images_non_intrusive function returns a False when the
        # image have the metadata corresponding to an Intrusive Image
        img = Image.new('RGB', (30, 30), color='red')
        meta = PngInfo()
        meta.add_text("jfif", "444")
        image_path = '/home/datasci/PycharmProjects/pac4/test_img_intrusive.png'
        img.save(image_path, "PNG", pnginfo=meta)

        self.assertEqual(Validation.check_intrusive_images(image_path), False)


unittest.main(argv=['first-arg-is-ignored'], verbosity=2, exit=False)
