Template script to perform TeraChem Cloud calculations starting from a picture of a hand-drawn chemical structure 

This folder contains: 
-) requirements.txt, 
-) main.py, # It requires credentials for TCC and Mathpix  
-) test images (test1.jpg, test2.jpg, test3.jpg)

Requires Python 3.8 or newer

Instructions:

# Creating a virtual environment
python3 -m venv env

# Activating a virtual environment
source env/bin/activate

# Installing python packages 
pip install -r requirements.txt 

# Executing the script  

python3 main.py test1.jpg 

# Deactivating the environment 
deactivate
