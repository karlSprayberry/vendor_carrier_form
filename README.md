# account-request-website
## Project Overview
account-request-website is an API that assists Rheem in submitting new account requests to the *Reliance* system. The page collects information pertaining 
to the Reliance application VACATION5 under the document USER_PROFILE_TEST_D. This API is currently hosted in Heroku and the current site can be found 
[here](https://account-request-website.herokuapp.com). This API currently works with *Reliance 2020a.5*. For customization for the *Reliance* team, two major 
files we focus on for development are **index.html** and **main.py**.

## index.html
Index.html is the main html file for the API. By default this page loads, and is the main source for submitting info for the new account. This file contains 
links to import the CSS files and additional styling. There is a single angular script section that launches the application.

## main.py
Main.py is the python file that handles both the page transitioning and the submission of the information collected to the *Reliance* system. This file
is launched before the index.html file is initialized. The file is divided by app routes, which in turn have functions. You can access the pages by adding
parameters of the route to the main website link. The '/create' route handles the creation of the object that has all of the info that is sent to
the *Reliance* system. A note here is that the fields collected are hard coded, so if a change is made to USER_PROFILE_TEST_D, it will not show up here.
