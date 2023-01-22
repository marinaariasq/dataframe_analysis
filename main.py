import pandas as pd
import os

from validation import Validation
from processor import Processor
from graph_generator import GraphGenerator
from popularity_analyzer import PopularityAnalyzer
from csv_creator import CsvCreator

IMAGE_FILE_FORMAT = '.png'
PATH_LABELS_FILES_FOLDER = "./dataset_cities/labels/"
PATH_IMAGES_FILES_FOLDER = "./dataset_cities/images/"

IMAGE_WIDTH_IN_PIXELS = 2048
IMAGE_HEIGHT_IN_PIXELS = 1024

# allows all columns in the pandas data frame to be visible
pd.set_option('display.max_columns', None)

# names of each .txt file of the labels directory
list_labels = [file for file in os.listdir(PATH_LABELS_FILES_FOLDER) if file.endswith('.txt')]

PATH_FILE_CLASS_NAME = "./dataset_cities/class_name.txt"
dict_class_names = {}

# make a dictionary from class_name.txt
with open(PATH_FILE_CLASS_NAME, 'r') as file:
    for line in file:
        key, value = line.strip().split(" ", 1)
        dict_class_names[int(key)] = value

data = []
corrupt_files_names = []
# Loop through each file in list_labels
for file in list_labels:
    #  find the .txt file with the specified label name
    file_path = os.path.join(PATH_LABELS_FILES_FOLDER, file)
    #  checks if the .txt file is in yolo format, and if so, adds the information to the dataframe
    if Validation.check_yolo(file_path):
        df = pd.read_csv(file_path, delimiter=' ',
                         names=['object_id', 'coord_x', 'coord_y', 'rect_w', 'rect_h', 'YOLO_prob'])

        df['file_name'] = file
        df['city_name'] = file.split("_")[0]

        # Add the object_name to the DataFrame using the object_id and dict_class_names
        df['object_name'] = df['object_id'].map(dict_class_names)

        # Append the data from the file to the list
        data.append(df)
    else:
        corrupt_files_names.append(file)

print('\t Theoretical answer to exercise 1.2 \n')
print('In the case of working with a huge set of images and files, it will be necessary to divide this set of '
      'information by chunks so that it can be processed by several threads or multiprocessors.\n'
      'In this way, each of the threads or multiprocessors will be able to simultaneously process its corresponding '
      'part of the information concurrently. \nThe result will be an increase in processing speed and less chance of '
      'running out of memory. \n')

# Concatenate all the data into a single DataFrame
df_image_objects = pd.concat(data)

print('Resulting data frame: \n')
print(df_image_objects.head(10))

print('Corrupted files that do not follow the YOLO format: \n {}'.format(corrupt_files_names))

print("----------")
processor = Processor()
label_names_first_image_by_city = processor.get_first_image_by_city_file_name(df_image_objects)
print("Showing in figures the detection of objects of the following images: {}".format(label_names_first_image_by_city))

graphGenerator = GraphGenerator()
for file_name in label_names_first_image_by_city:
    image_objects = processor.get_image_objects_by_file_name(df_image_objects, file_name)
    image_file_name = graphGenerator.get_image_name_from_file_name(file_name)
    graphGenerator.draw_image_with_object_rectangles(image_file_name, image_objects)

print("----------")
df_image_objects_high_yolo = processor.filter_dataframe_by_high_yolo(df_image_objects)
df_objectID_count = processor.get_object_id_count_of_dataframe(df_image_objects_high_yolo)
df_top_5_objectsID = df_objectID_count.iloc[0:5]
print("The 5 most detected objects in the dataset ¡ : \n")
print(df_top_5_objectsID.iloc[0:5])
graphGenerator.draw_graph_total_count_object_id(df_objectID_count)

print("----------")

print("Plot normalized histogram of top 5 objects")
df_objectID_counts_by_file = processor.get_objectname_count_by_file(df_image_objects_high_yolo)
top5_object_names = df_top_5_objectsID['object_name']
graphGenerator.draw_graph_total_count_top5_objects_by_file(df_objectID_counts_by_file, top5_object_names)
print('\t Explanation of the obtained histogram graph')
print('If we analyze the frequency histogram obtained we see that:\n' +
      '- The car object is the most frequently detected object with the maximum number of times in one image (20)'
      'compared to the other objects.\n' +
      '- The truck object is the most frequently detected only once compared to the other objects.\n' +
      '- For all objects the most frequent is that they are detected only once per image.\n' +
      'If we analyze in detail:\n' +
      '\t Cars: can be detected from 0 to 20 times per image.\n' +
      '\t Person: can be detected between 0-16 to 19-20 times per image.\n' +
      '\t Bicycle: can be detected from 0 to 6 times per image.:\n' +
      '\t Traffic light: can be detected from 0 to 6 times per image.\n' +
      '\t Truck: can be detected from 0 to 4 times per image.\n')

print("----------")

average_total_object_detection_by_file = processor.average_number_objects_by_file(df_image_objects_high_yolo)
print("The average number of objects detected per image is a total of {} objects.".format(
    average_total_object_detection_by_file))

print("----------")
popularity_analyzer = PopularityAnalyzer()
ordered_popularity_dictionary = popularity_analyzer.get_popularity_of_objects(df_image_objects_high_yolo)
print('The dictionary popularity: \n {} \n'.format(ordered_popularity_dictionary))
print(
    'We can see that the three most popular items in each image match the three most popular items in the hole '
    'dataset.\nNext I will show on screen a case in which the image does not contain any of the three most popular '
    'elements:\n')
df_without_popular_objects = popularity_analyzer.get_df_without_top3_popular_objects(df_image_objects_high_yolo)
print(df_without_popular_objects)

print("----------")
#  filter dataframe with only cars as objects_name
df_car_only = df_image_objects_high_yolo.loc[df_image_objects_high_yolo['object_name'] == 'car']
# make a copy in order to not work with views of the original dataframe
df_car_only = df_car_only.copy()
df_maco = processor.get_objectname_count_by_file(df_car_only)
df_cars_with_city_year_columns = processor.insert_city_year_to_df(df_maco)
print('Graphic representation of the total number of cars counted by city and year')
graphGenerator.draw_graph_total_cars_by_city_and_year(df_maco)

print("----------")

image_type_dataframe = df_image_objects_high_yolo.assign(Image_type=' ')
label_names_first_image_by_city = image_type_dataframe['file_name'].tolist()
intrusive_files = []
for file in label_names_first_image_by_city:
    img_file = file.replace(".txt", IMAGE_FILE_FORMAT)
    img_path = os.path.join(PATH_IMAGES_FILES_FOLDER, img_file)
    if not Validation.check_intrusive_images(img_path):
        type_image = 'Intrusive Image'
        image_type_dataframe.loc[image_type_dataframe['file_name'] == file, 'Image_type'] = type_image
        intrusive_files.append(img_file)
    else:
        type_image = 'City Image'
        image_type_dataframe.loc[image_type_dataframe['file_name'] == file, 'Image_type'] = type_image

print('Intrusive images detected: \n {} \n '.format(intrusive_files))
print('\t Explanation of the method I have implemented to detect which images are intrusive: \n')
print(
    'To find the intrusive images I have analyzed the information present in the metadata of each image. To access the '
    'metadata of each image I used the PIL library.\n'
    'First, I have made an inspection of the "Images" folder and I have studied the metadata of 3 intrusive images and '
    '3 images of cities that I have detected visually by applying the ".info()" function. \n'
    'While comparing the information in each group of images I recognized a different pattern of metadata information '
    'between the city images and the intrusive images.\nThis difference is that the intrusive image has a "jfif" '
    'parameter in its metadata which is missing in the metadata of the city images. \n'
    'Consequently, to detect which images are intrusive or not, I have studied the metadata of each image detecting '
    'if they do not have this parameter specified (city image) or if they do (intrusive image). ')

print('-------')

csv_creator = CsvCreator()
csv_name, path_csv = csv_creator.create_csv_file_from_df(image_type_dataframe, 'images_information.csv')
print('The generated csv file is named as {} and has been stored in the following path {} '.format(csv_name, path_csv))
