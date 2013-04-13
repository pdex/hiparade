import logging
from sleekxmpp import ClientXMPP

class Client(ClientXMPP):
    def __init__(self, jid, password, on_receive, rooms):
        ClientXMPP.__init__(self, jid, password)

        self.rooms = rooms
        self.rooms_by_name = {v: k for k, v in rooms.items()}
        self.on_receive = on_receive
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            room = self.rooms.get(msg['from'].bare, None)
            if room is not None:
                self.on_receive(room, msg['body'])

    def start(self):
        self.connect()
        self.process(block=False)

    def stopThePresses(self):
        self.disconnect()

    def send_to_room(self, room, msg):
        jid = self.rooms_by_name.get(room, None)
        if jid is not None:
            self.send_message(mto=jid, mbody=msg)


class MucClient(Client):

    def __init__(self, jid, password, on_receive, rooms, nick):
        super(MucClient, self).__init__(jid, password, on_receive, rooms)
        self.nick = nick
        self.add_event_handler("groupchat_message", self.muc_message)
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0199') # XMPP Ping


    def session_start(self, event):
        super(MucClient, self).session_start(event)
        for room in self.rooms:
            self.plugin['xep_0045'].joinMUC(
                room,
                self.nick,
                wait=True
            )
    def muc_message(self, msg):
        """
        Process incoming message stanzas from any chat room. Be aware
        that if you also have any handlers for the 'message' event,
        message stanzas may be processed by both handlers, so check
        the 'type' attribute when using a 'message' event handler.

        IMPORTANT: Always check that a message is not from yourself,
                   otherwise you will create an infinite loop responding
                   to your own messages.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['mucnick'] != self.nick:
            room = self.rooms.get(msg['mucroom'], None)
            if room is not None:
                message = "%(mucnick)s: %(body)s" % msg
                self.on_receive(room, message)

    def keepalive(self):
        self.send_presence(pstatus='hit me')

    def send_to_room(self, room, msg):
        jid = self.rooms_by_name.get(room, None)
        if jid is not None:
            self.send_message(
                mto=jid,
                mbody=msg,
                mtype='groupchat'
            )
