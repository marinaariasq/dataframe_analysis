import matplotlib
import matplotlib.pyplot as plt

PATH_IMAGES_FILES_FOLDER = "./dataset_cities/images/"
IMAGE_FILE_FORMAT = '.png'

IMAGE_HEIGHT_IN_PIXELS = 1024
IMAGE_WIDTH_IN_PIXELS = 2048


class GraphGenerator:

    def get_image_name_from_file_name(self, file_name):
        return file_name.split('.')[0] + IMAGE_FILE_FORMAT

    def __un_normalize(self, coord, dim_pixels):
        return coord * dim_pixels

    def draw_image_with_object_rectangles(self, image_file_name, image_objects):
        img = matplotlib.image.imread(PATH_IMAGES_FILES_FOLDER + image_file_name)

        figure, ax = plt.subplots()
        ax.imshow(img)

        for index, image_object_row in image_objects.iterrows():
            x = self.__un_normalize(float(image_object_row['coord_x']), IMAGE_WIDTH_IN_PIXELS)
            y = self.__un_normalize(float(image_object_row['coord_y']), IMAGE_HEIGHT_IN_PIXELS)
            w = self.__un_normalize(float(image_object_row['rect_w']), IMAGE_WIDTH_IN_PIXELS)
            h = self.__un_normalize(float(image_object_row['rect_h']), IMAGE_HEIGHT_IN_PIXELS)

            rect = matplotlib.patches.Rectangle((x - w / 2, y - h / 2), w, h, edgecolor='r', facecolor="none")
            ax.add_patch(rect)

        plt.show()
        return

    def draw_graph_total_count_object_id(self, df):
        plt.bar(df["object_name"], df["count"])
        plt.title("Total number of each class object")
        plt.xticks(rotation='vertical')
        plt.ylabel("Count")
        plt.show()
        return

    def draw_graph_total_count_top5_objects_by_file(self, df, top5_object_names):
        df_top_objects_by_file = df[df['object_name'].isin(top5_object_names)]
        df_top_objects_by_file.groupby(['file_name', 'object_name'])['count'].sum().unstack().plot.hist(stacked=True)
        plt.ylabel('frequency')
        plt.xlabel('total number that the object appears in the image')
        plt.title('frequency of occurrence of the 5 most popular objects in all images')
        plt.show()
        return

    def draw_graph_total_cars_by_city_and_year(self, df):
        df.groupby(['city', 'year'])['count'].sum().unstack().plot(kind='bar')
        plt.ylabel('count')
        plt.xlabel('City')
        plt.title('Counted cars by city and year')
        plt.show()
        return
