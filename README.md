# warbler-flaskbp

Deployed on: https://sanchez-warbler.onrender.com

*Please be patient, render is slow to load.

# To host locally

Create virtual environment and activate:

`python3 -m venv venv`

`source venv/bin/activate`

Install dependencies and run app:

`pip3 install -r requirements.txt`

Install warbler app as a python package in the top level directory (app)

`pip3 install -e .`

After installing nums_api delete the nums_api.egg-info/ directory

`rm -rf nums_api.egg-info/`

Run app

`python3 -m flask run -p 5000`

# To containerize app

Follow instructions in docker-setup.md
