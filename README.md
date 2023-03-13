# warbler-flaskbp

Deployed on: https://sanchez-flask-warbler.onrender.com

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

When you need to add dependencies to requirements.txt, don't include the
nums_api package as a dependency. To ensure it's not added, update
requirements.txt like this

`pip3 freeze | grep -v github.com > requirements.txt`

Run app

`python3 -m flask run -p 5000`
