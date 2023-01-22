import matplotlib
import matplotlib.pyplot as plt

PATH_IMAGES_FILES_FOLDER = "./dataset_cities/images/"
IMAGE_FILE_FORMAT = '.png'

IMAGE_HEIGHT_IN_PIXELS = 1024
IMAGE_WIDTH_IN_PIXELS = 2048


class GraphGenerator:

    def get_image_name_from_file_name(self, file_name):
        """
        This function replaces the substring .txt with the substring .png of the main string file_name.

        Inputs:
        file_name: [string] name of the .txt file

        Outputs:
        file_name: [string] name of the file as .png.
        """
        return file_name.split('.')[0] + IMAGE_FILE_FORMAT

    def __denormalize(self, coord, dim_pixels):
        """
        This function denormalize the coordinates from the dataframe using the pixels dimension.

        Inputs:
        coord: [int] coordinate
        dim_pixels: [int] dimension of the pixel

        Outputs:
        coord * dim_pixels: [int] coordinates denormalized
        """
        return coord * dim_pixels

    def draw_image_with_object_rectangles(self, image_file_name, image_objects):
        """
        This function draws rectangles that frame the detected id_objects in a specified image.

        Inputs:
        image_file_name: [str] name of the image file.
        image_objects: [pandas dataframe] original dataframe containing the data.

        Outputs:
        None
        """
        img = matplotlib.image.imread(PATH_IMAGES_FILES_FOLDER + image_file_name)

        figure, ax = plt.subplots()
        ax.imshow(img)

        for index, image_object_row in image_objects.iterrows():
            x = self.__denormalize(float(image_object_row['coord_x']), IMAGE_WIDTH_IN_PIXELS)
            y = self.__denormalize(float(image_object_row['coord_y']), IMAGE_HEIGHT_IN_PIXELS)
            w = self.__denormalize(float(image_object_row['rect_w']), IMAGE_WIDTH_IN_PIXELS)
            h = self.__denormalize(float(image_object_row['rect_h']), IMAGE_HEIGHT_IN_PIXELS)

            rect = matplotlib.patches.Rectangle((x - w / 2, y - h / 2), w, h, edgecolor='r', facecolor="none")
            ax.add_patch(rect)

        plt.show()
        return

    def draw_graph_total_count_object_id(self, df):
        """
        This function generates a bar graph representing the number of times each object_name appears in the original
        dataframe.

        Inputs:
        df: [pandas dataframe] original dataframe containing the data.

        Outputs:
        None
        """
        plt.bar(df["object_name"], df["count"])
        plt.title("Total number of each class object")
        plt.xticks(rotation='vertical')
        plt.ylabel("Count")
        plt.show()
        return

    def draw_graph_total_count_top5_objects_by_file(self, df, top5_object_names):
        """
        this function generates a normalized histogram that will represent the frequency of occurrence of the most
        popular object_names in the dataframe for each file_name.

        Inputs:
        df: [pandas dataframe] original dataframe containing the data.
        top5_object_names: [list] the 5 object_name that appear most often in the dataframe

        Outputs:
        None
        """
        df_top_objects_by_file = df[df['object_name'].isin(top5_object_names)]
        df_top_objects_by_file.groupby(['file_name', 'object_name'])['count'].sum().unstack().plot.hist(stacked=True)
        plt.ylabel('frequency')
        plt.xlabel('total number that the object appears in the image')
        plt.title('frequency of occurrence of the 5 most popular objects in all images')
        plt.show()
        return

    def draw_graph_total_cars_by_city_and_year(self, df):
        """
        This function generates a bar chart representing the number of times cars appear depending on the city and year
         in the original data frame.

        Inputs:
        df: [pandas dataframe] original dataframe containing the data.

        Outputs:
        None
        """
        df.groupby(['city', 'year'])['count'].sum().unstack().plot(kind='bar')
        plt.ylabel('count')
        plt.xlabel('City')
        plt.title('Counted cars by city and year')
        plt.show()
        return
