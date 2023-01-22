
First set up files:
1. unzip <ZIP_NAME>.zip -d ./pac4_marina_arias
2. cd test2/

3. mv <PATH_OF_DATASET_CITIES> ./

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

