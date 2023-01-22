import pandas as pd
import os
import csv

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

# TODO remove? used for prints
pd.set_option('display.max_columns', None)

# names of each .txt file of the labels directory
list_labels = [file for file in os.listdir(PATH_LABELS_FILES_FOLDER) if file.endswith('.txt')]

PATH_FILE_CLASS_NAME = "./dataset_cities/class_name.txt"
dict_class_names = {}

with open(PATH_FILE_CLASS_NAME, 'r') as f:
    # Loop through each line in the file
    for line in f:
        # Split the line into key and value
        key, value = line.strip().split(" ", 1)
        # Add the key-value pair to the dictionary
        dict_class_names[int(key)] = value

data = []
# Loop through each file in list_labels
corrupt_files_names = []
for file in list_labels:
    file_path = os.path.join(PATH_LABELS_FILES_FOLDER, file)
    if Validation.check_yolo(file_path):
        # Read the contents of the file into a DataFrame
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

print('Corrupt files:')
print(corrupt_files_names)

# Concatenate all the data into a single DataFrame
df_image_objects = pd.concat(data)

print('Resulting data frame:')
print(df_image_objects)

print("Size of final dataframe : {}".format(df_image_objects.shape))

print("----------")
processor = Processor()
label_file_names = processor.get_first_image_by_city_file_name(df_image_objects)
print("Showing in figures the detection of objects of the following images: {}".format(label_file_names))

graphGenerator = GraphGenerator()
for file_name in label_file_names:
    image_objects = processor.get_image_objects_by_label_file_name(df_image_objects, file_name)
    image_file_name = graphGenerator.get_image_name_from_file_name(file_name)
    graphGenerator.draw_image_with_object_rectangles(image_file_name, image_objects)

print("----------")

df_image_objects_high_yolo = processor.filter_dataframe_by_high_yolo(df_image_objects)
df_objectID_count = processor.get_object_id_count_of_dataframe(df_image_objects_high_yolo)
df_top_5_objectsID = df_objectID_count.iloc[0:5]
print("Top 5 detected objects in the dataset : \n")
print(df_top_5_objectsID.iloc[0:5])
graphGenerator.draw_graph_total_count_object_id(df_objectID_count)

print("----------")

print("Plot normalized histogram of top 5 objects")
df_objectID_counts_by_file = processor.get_objectname_count_by_file(df_image_objects_high_yolo)
top5_object_names = df_top_5_objectsID['object_name']
graphGenerator.draw_graph_total_count_top5_objects_by_file(df_objectID_counts_by_file, top5_object_names)

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
    'Podem veure que els tres elements més populars per imatge coincideixen amb els tres elements més populars del'
    'dataset.\n' +
    'A continuació mostrare en pantalla un cas en que la imatge no conté ningun dels tres elements més populars: \n')
df_without_popular_objects = popularity_analyzer.get_df_without_top3_popular_objects(df_image_objects_high_yolo)
print(df_without_popular_objects)

print("----------")

df_car_only = df_image_objects_high_yolo.loc[df_image_objects_high_yolo['object_name'] == 'car']
# make a copy in order to not work with views of the original dataframe
df_car_only = df_car_only.copy()
df_maco = processor.get_objectname_count_by_file(df_car_only)
df_cars_with_city_year_columns = processor.insert_city_year_to_df(df_maco)
print('Graphic representation of the total number of cars counted by city and year')
graphGenerator.draw_graph_total_cars_by_city_and_year(df_maco)

print("----------")

imagetype_dataframe = df_image_objects_high_yolo.assign(Image_type=' ')
label_file_names = imagetype_dataframe['file_name'].tolist()
intrusive_files = []
for file in label_file_names:
    img_file = file.replace(".txt", IMAGE_FILE_FORMAT)
    img_path = os.path.join(PATH_IMAGES_FILES_FOLDER, img_file)
    if not Validation.check_intrusive_images(img_path):
        type_image = 'Intrusive Image'
        imagetype_dataframe.loc[imagetype_dataframe['file_name'] == file, 'Image_type'] = type_image
        intrusive_files.append(img_file)
    else:
        type_image = 'City Image'
        imagetype_dataframe.loc[imagetype_dataframe['file_name'] == file, 'Image_type'] = type_image

print('Intrusive images detected: \n {} \n '.format(intrusive_files))

# TODO : traduce the text
print(
    'Per trobar les images intruses he analitzat la informació que es trobava present a les metadates.Per tal de'
    'poder accedir a aquesta informació' +
    'he fet ús de la llibreria PIL. \n Primer he fet una inspecció visual de la carpeta "Images" i he copiat la ruta '
    'de 3 imatges intruses i 3 imatges de ciutats' +
    'que he detectat. \n Posteriorment mitjançant PIL he analitzat les metadades de cada imatge a partir de la funció '
    '.info(). \n En analitzar la informació obtinguda' +
    'he pogut detectar que les imatges intruses tenien parametres comuns en les seves metadades que no tenien les'
    'imatges de ciutat. \n Un dels paràmetres es el ' +
    '"jfif" que es el que he utilitzat a posteriori per detectar les imatges del dataset que no son imatges de '
    'ciutat. \n Per tal de fer aquesta detecció he generat una funció de validació que ' +
    'comprova si el parametre "jfif" esta en les metadades de la imatge, en el cas que no estigui faig que la funció '
    'retorni True i en cas que si que retorni False. \n  El valor que retorni la funció' +
    'el faré servir per determinar si és o no és intrusa la imatge i afegir aquesta informació tant al dataframe com '
    'a la llista de imatges intruses')

print('-------')

csv_creator = CsvCreator()
csv_name, path_csv = csv_creator.create_csv_file_from_df(imagetype_dataframe, 'images_information.csv')
print('The generated csv file is named as {} and has been stored in the following path {} '.format(csv_name, path_csv))
