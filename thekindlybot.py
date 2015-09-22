
import sys
import logging
import getpass
from optparse import OptionParser
from creds import *
import sleekxmpp
from hangman import *
from eliza import eliza as AI
import re
from weather import *
# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class Slackbot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.therapist=AI()
        self.hangman=Game()

    def start(self, event):

        self.send_presence(pstatus="Hello, I am a chat bot. I like playing Hangman. Type '$help' for help.")
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            user,text=msg['from'],msg['body']
            gameon = user in self.hangman.playertable
            if text[0]=='$'  and  not gameon:
                to_send=self.process_message(user,text[1:].strip().lower())
            elif gameon :
                to_send=self.hangman.gameresponse(text.lower(), user) if text[0]!='$' or len(text)==1 else self.process_message(user,text[1:].strip().lower())
            else:
                to_send=self.therapist.respond(text)
            msg.reply(to_send).send()

    def process_message(self,user,command):
        if command=='help':
            return '''$start hangman to start a game of hangman. Enter one character at a time. 
$stop hangman to stop it.
$whaddup <cityname> for a weather report. eg. $whaddup london 
I talk normally as well.'''
        elif command=='start hangman':
            self.hangman.cleanup()
            self.hangman.register_player(user)
            return self.hangman.startgame(user)
        elif command =='stop hangman' :
            return self.hangman.delete_player(user)
        elif command.split()[0] == 'whaddup' and len(command)>1:
            location=' '.join(command.split()[1:])
            report=get_report(location)
            return report

        



if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')
    xmpp = Slackbot(jid, password)
    # xmpp.register_plugin('xep_0030') # Service Discovery
    # xmpp.register_plugin('xep_0004') # Data Forms
    # xmpp.register_plugin('xep_0060') # PubSub
    # xmpp.register_plugin('xep_0199') # XMPP Ping
    # xmpp.connect((xmppserver, port))
    xmpp.connect()
    xmpp.process(block=True)