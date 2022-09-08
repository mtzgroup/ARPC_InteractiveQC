This is an interactive application to perform quantum chemical calculation on Twitter. 
By tweeting @TerachemBot compute [property][molecule][functional], the Twitter bot will pick up the request and 
reply to the tweet with the results of the prompted calculation. 
TerachemBot can perform single point energy calculations with different density functionals (the basis set is fixed for simplicity to 3-21G) 
and return the self-consistent energy or dipole moment. Its workflow is simple: 
(i) retrieve mentions via Twitter API, 
(ii) parse the input information and launch the calculation on TeraChem Cloud, 
(iii) send back the calculation results via the Twitter API. 

Currently the bot is offline, however, a video showing TeraChemBot in action is provided here (https://youtu.be/yrpVwqvSk-w).

This script requires credentials for TCC and Twippy   

Requires Python 3.8 or newer

python3 main.py 

