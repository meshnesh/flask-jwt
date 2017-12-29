# Bright Events 

[![Build Status](https://travis-ci.org/meshnesh/flask-jwt.svg?branch=master)](https://travis-ci.org/meshnesh/flask-jwt)


An events platform where people create new events and share with others. One can see how many people are reserved to there event.

Events contain locations, time and day when it will happen, user can logging in and them to there list if they are available to attend.

### Wireframes Designs ###
The platform is being developed from this designs

![Alt homepage](https://github.com/meshnesh/meshnesh.github.io/blob/master/designs/wireframes/bright_events_homepage.png)
![Alt sign-in](https://github.com/meshnesh/meshnesh.github.io/blob/master/designs/wireframes/SIGN%20IN.png)
![Alt login](https://github.com/meshnesh/meshnesh.github.io/blob/master/designs/wireframes/Login.png)
![Alt event details](https://github.com/meshnesh/meshnesh.github.io/blob/master/designs/wireframes/desktop_card_page.png)

## UI Designs ##
* All the front-end development files are located with in the designs folder, so are the wireframes and the uml-class and wireframes of the respective pages

You can also view the [UI](https://meshnesh.github.io/designs/ui/) here.

### uml-class diagram ###
![Alt Uml-diagram](https://github.com/meshnesh/Bright-Events/blob/develop/designs/uml_diagram/Bright%20Events.png)

## To run the flask api  ##
* clone the repo:

 ``` git clone https://github.com/meshnesh/Bright-Events.git ```

* change the directory to the project:

``` cd Bright-Events ```

Create a virtual enviroment and install all the dependacy modules, in to your machine

* To create a virtual enviroment run

    ``` virtualenv -p python3 myenv```

* Activating the enviroment

    ``` source venv/bin/activate```


Install all dependancies for the project by running:

``` sudo apt install pip```

on your terminal run

``` pip install -r requirements.txt ```

# run 
To test our project on your terminal run 

``` export FLASK_APP=run.py```

then

``` flask run ```

Open: [http://127.0.0.1:5000/api/events](http://127.0.0.1:5000/api/events)

# Heroku App
View the application on heroku:
Open: [Bright Events](https://bright-events.herokuapp.com/api/events)
