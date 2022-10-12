from app.rest import app, api

from app.rest.user import *
from app.rest.song import *
from app.rest.genre import *
from app.rest.album import *
from app.rest.artist import *


if __name__ == '__main__':
    app.run(debug=True, port=5000)
