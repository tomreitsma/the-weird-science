# The Weird Science

A simple multiplayer Tetris clone built in Javascript and Python

### Setup instructions

- Linux:
    - `apt-get install python-pip`
    - `pip install virtualenv`
    - `virtualenv theweirdscience && cd theweirdscience`
    - `git clone https://github.com/tomreitsma/the-weird-science.git app`
    - `cd app && source ../bin/activate`
    - `./setup.sh`
    - `python server.py`

You should now be able to access The Weird Tetris on http://localhost:8080

If you wish to gain access from a host other than localhost edit the following:

Change `WEBSOCKET_HOST` in ./public/js/config.js to your network ip

Change `WEBSOCKET_HOST` in ./settings.py to your network ip

### Controls

Arrow keys left, right and down to move the piece. Arrow key up to rotate the piece. 
Press enter to disable the music.