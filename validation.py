import csv
from PIL import Image


class Validation:


    @staticmethod
    def check_yolo(path_file):
        """
        This function checks the validity of a file located at 'path_file'. The file is in the format of a CSV with 6
        columns, where the first column must be an integer between 0 and 80, and the remaining 5 columns must be
        floats between 0 and 1. If the file is invalid, the function returns False, otherwise it returns True.
        """

        with open(path_file, 'r') as f:
            file_rows = csv.reader(f, delimiter=' ')
            for row in file_rows:
                if len(row) != 6:
                    return False

                for idx, value in enumerate(row):
                    if idx == 0:
                        if value.isdigit():
                            value_int = int(value)
                            if value_int > 80 or value_int < 0:
                                return False
                        else:
                            return False
                    else:
                        try:
                            value = float(value)
                        except:
                            return False
                        if value < 0 or value > 1:
                            return False
        return True

    @staticmethod
    def check_intrusive_images(img_path):
        """
        This function checks if an image located at 'img_path' is an intrusive image. The function uses the Pillow
        library to open the image, and checks if the 'jfif' marker is present in the image. If the marker is present,
        the function returns False, indicating that the image is intrusive. Otherwise, it returns True.
        """
        with Image.open(img_path) as img:
            if 'jfif' in img.info:
                return False
            return True
