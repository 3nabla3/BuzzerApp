# Buzzer app
## General preconditions
This section requires the following preconditions:

You have python 3.x installed and runnable with the following command
* Windows
  * `> py`
* Linux
  * `$ python3`
   
You have pip installed for the specific version of python 3.x and runnable with the following command 
* Windows
  * `> py -m pip`
* Linux
  * `$ python3 -m pip`

## Download and install Flask
Download and install Flask using pip with this command
* Windows
  * `> py -m pip install flask`
* Linux
  * `$ python3 -m pip install flask`

## Running the app
* Windows
1) `> py -m pip install flask`
2) `> set FLASK_ENV=development`
3) `> py -m flask run --host=<your local IP address>`

* Linux
1) `$ python3 -m pip install flask`
2) `$ export FLASK_ENV=development`
3) `$ python3 -m flask run --host=0.0.0.0`

