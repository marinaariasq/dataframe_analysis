
This ZIP file contains all the files that give answer to the PAC4 of the course "Programming for Data Science" 
of the UOC 2022-2023.
In this project a set of .txt files and .png images will be analyzed in order to generate a database. 
Subsequently, the obtained database will be studied in order to extract valuable information.


THIS ZIP FILE CONTAINS THE FOLLOWING FILES:

  - README.txt: Text file that contains all the information in order to execute this project.

  - Requirements.txt: Text file containing all the libraries that must be installed in the virtual 
    environment in order for the project to be executed.

  - LICENSE : License used in this project

  - "main.py": This file contains the code that gives the PAC4 solutions. 
     This code uses functions that use classes defined in other .py files.
     Therefore, to see the PAC solutions run this file.

     Python files where the classes containing the functions that are subsequently applied to 
     the main.py file are defined:

    	- "validation.py": This file contains the Validation class which contains the functions that are in 
       	charge of validating the dataframe and images

	- "processor.py": This file contains the Processor class that contains the functions that are in 
	charge of preprocessing the dataframe in order to obtain a dataframe that follows certain conditions.

	- "graph_generator.py": This file contains the GraphGenerator class that contains the functions that
	are in charge of generating graphical representations of the dataframe and drawing the object 
	detection rectangles on the images.

	- "csv_creator.py": This file contains the CsvCreator class that contains the function that 
	creates the csv file asked in exercice 7.


	   Python files containing the tests that evaluate the functionality of the functions coming from 
	   the classes defined in the 4 python files mentioned above:

		- "test_validation.py": This file contains the test to evaluate the functions of the Validation 
		   class of the Validation.py file.

		- "test_processor.py": This file contains the test to evaluate the functions of the Processor 
		   class of the processor.py file.
		- "test_graph_generator.py": This file contains the test to evaluate the functions of the 
		   GraphGenerator class of the graph_generator.py file.

		- "test_csv_creator.py": This file contains the test to evaluate the functions of the CsvCreator 
		   class of the csv_creator.py file.


- HOW TO EXECUTE PAC4:

First set up files:
1. unzip <ZIP_NAME>.zip -d ./pac4_marina_arias
2. cd pac4_marina_arias/

3. mv <PATH_OF_DATASET_CITIES> ./pac4_marina_arias

With folder hierarchy:
./dataset_cities
--/images
--/labels
--class_name.txt

Then setup environmnt

1. python3 -m venv .venv

(You might need to install before: sudo apt install python3.8-venv)

2. source .venv/bin/activate
3. pip install -r requirements.txt 

Then, to run the program:
python3 main.py 

And to run tests and see results:
1. coverage run -m unittest discover
2. coverage report

