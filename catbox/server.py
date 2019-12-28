"""
server
====================================================================================================

Management of an instance of the server, allows creating and managing games.

----------------------------------------------------------------------------------------------------

**Created**
    2019-12-28
**Updated**
    2019-12-28 by Darkar
**Author**
    WildfireXIII
**Copyright**
    This software is Free and Open Source for any purpose
"""

import logging
import string
import random

from flask_socketio import SocketIO


class Server():
    """ Core server class """

    _room_code_length = 4
    """ Number of characters in a room code """

    def __init__(self, app):
        self.app = app
        self.socketio = SocketIO(self.app)
        self.client_sids = []

        self.games = {}  # associate room codes with game instances

        self.socketio.on_event("connect", self.handle_connect)
        self.socketio.on_event("disconnect", self.handle_disconnect)
        self.socketio.on_event("join", self.handle_join)

        logging.info("Server initialized")

    def create_code(self):
        """ Create a short room code for joining the game """
        return "".join([random.choice(string.ascii_uppercase + string.digits) for _ in
                        range(Server._room_code_length)])

    def register_game(self, game):
        """ Register the instance of Game with the server and start hosting it """

        # search for unused code TODO find a non-evil way of doing this
        code = self.create_code()
        while code in self.games:
            logging.debug("Code %s in use, regenerating", code)
            code = self.create_code()

        self.games[code] = game
        game.server = self
        game.code = code

        logging.info("Game with code %s created", code)

    def handle_connect(self, request):
        """ Allow clients to connect to the server """
        logging.info("Client %s connected", request.sid)
        self.client_sids.append(request.sid)

    def handle_disconnect(self, request):
        """ Allow clients to disconnect from the server """
        logging.info("Client %s disconnected", request.sid)
        self.client_sids.remove(request.sid)

    def handle_join(self, json):
        """ Connect a client with a game """
        logging.info("User '%s' (name '%s') requesting to join room '%s'", request.sid, json["username"], json["code"])
        

    def communicate(self, sid, event, data):
        """ Sends the event and data to the client with the sid """
        logging.debug("Emitting %s to %s", event, sid)
        self.socketio.emit(event, data, room=sid)