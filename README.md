# Warbler
Twitter clone - users can post/like messages and follow other users.

Deployed on: https://sanchez-warbler.onrender.com  
*Please be patient, render is slow to load.

## Local Setup

1. Navigate to `app/`. Create virtual environment and activate.

    ```
    cd app/  
    python3 -m venv venv  
    source venv/bin/activate
    ```

2. Install dependencies.

    ```
    pip3 install -r requirements.txt
    ```

3. Install warbler app as a python package. Then, remove the `warbler.egg-info` file.

    ```
    pip3 install -e .
    rm -rf warbler.egg-info/
    ```

4. Run app
    ```
    python3 -m flask run -p 5000
    ```

## Containerization

Follow instructions in `docker-setup.md`.

## TODO

- [ ] Incorporate instant messaging.
- [ ] Add additional 'like' logic to return back to previous page.
