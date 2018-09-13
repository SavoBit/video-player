#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=======================================================================================================================
#
#          FILE:  player.py
#
#         USAGE:  ./player  [--start]
#
#   DESCRIPTION: This sowftware should be installed at the client (player) side in order to start/stop the video client.
#                This player is consuming messages from actions exchange in order to switch up/down layers when a new action is applied over the flow.
#                This plater is consuming messages from commands exchange in order to know some instructions such as start the payer or stop it.
#                At list one file.sdp must be located at the same folder in which this script is.
#                It needs some dependences described at requeriments.
#
#       OPTIONS:  --start This player will start consuming messages from actions and commands exchanges. (Normally called from launch.sh)
#
#  REQUIREMENTS:  python 2.7, kombu 4.1.0 , gpac branch v0.6.1, openHEVC rext branch, xdotool
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Pablo Salva Garcia
#       COMPANY:  UWS
#       VERSION:  1.0
#       CREATED:  12/09/2017
#      REVISION:  ---
#=======================================================================================================================

import sys, os
import json
import ConfigParser
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from argparse import ArgumentParser


def value_from_section(section):
    dict1 = {}
    options = parser.options(section)
    for option in options:
        try:
            dict1[option] = parser.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

# Constants from config.ini file wich has been produced by configure.sh
if not os.path.exists('config.ini'):
    print "Error - Please, run configure.sh script before to start this player"
    exit()

parser = ConfigParser.ConfigParser()
parser.read('config.ini')

rabbit_ip = value_from_section('Player')['rabbit_server_ip']
rabbit_vhost = value_from_section('Player')['vhost']
rabbit_user = value_from_section('Player')['user']
rabbit_passw = value_from_section('Player')['password']

actions_exchange = value_from_section('Actions')['exchange']
actions_queue_name = value_from_section('Actions')['queue_name']
actions_binding_key = value_from_section('Actions')['binding_key']

commands_exchange = value_from_section('Commands')['exchange']
commands_queue_name = value_from_section('Commands')['queue_name']
commands_binding_key = value_from_section('Commands')['binding_key']


class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues
        self.last_command = ''
        self.current_sdp = ''

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message])]

    def on_message(self, body, message):
        # from exchange: actions queue: player_actions
        if message.delivery_info['routing_key'] == actions_queue_name or message.delivery_info['exchange'] == actions_exchange:
            message.ack()
            body_action = json.loads(body)
            action = body_action['Action'] if 'Action' in body_action.keys() else None
            self.process_player_action(action)
        # from exchange: commands queue: player_commands
        elif message.delivery_info['routing_key'] == commands_queue_name or message.delivery_info['exchange'] == commands_exchange:
            message.ack()
            self.process_player_command(json.loads(body))
        # Do nothing
        else:
            print'a non-vallid message has been received, info:\n {0}'.format(message.delivery_info)
            message.ack()

        #print json.dumps(message)
        #message.ack()

    def process_player_action(self, body):
        if body is None:
            print'a non-valid message has been received from actions exchange'
        elif body['actionType'] == "INSERT" and body['actionName'] == 'DROP' and body['state'] == 'SUCCESS':
            print "Switching down layer..."
            if self.last_command == 'start':
                cm = "xdotool search --name {0} windowactivate --sync key ctrl+l".format(self.current_sdp)
            else:
                cm = "xdotool ctrl+l"
            os.system(cm)
        elif body['actionType'] == "DELETE" and body['actionName'] == 'DROP' and body['state'] == 'SUCCESS':
            print "Switching up layer..."
            if self.last_command == 'start':
                cm = "xdotool search --name {0} windowactivate --sync key ctrl+h".format(self.current_sdp)
            else:
                cm = "xdotool ctrl+h"
            os.system(cm)
        else:
            print'a non-valid message has been received from actions exchange, info:\n {0}'.format(body)

    def process_player_command(self, body):
        if body['command'] == 'start' and self.last_command != 'start' and self.last_command != 'startfs':
            print 'Starting player...'
            self.last_command = 'start'
            self.current_sdp = body['data']
            cm = 'MP4Client {0} &'.format(self.current_sdp)
            os.system(cm)
        elif body['command'] == 'startfs' and self.last_command != 'start' and self.last_command != 'startfs':
            print 'Starting player in full screen...'
            self.last_command = 'startfs'
            self.current_sdp = body['data']
            cm = 'MP4Client {0} -fs &'.format(self.current_sdp)
            os.system(cm)
        elif (body['command'] == 'start' or body['command'] == 'startfs') and (self.last_command == 'start' or self.last_command == 'startfs'):
            print 'The player is already started'
        elif body['command'] == 'stop' or body['command'] == 'close':
            print 'Switching off player...'
            self.last_command = 'stop'
            cm2 = 'sudo pkill MP4Client'
            os.system(cm2)
        else:
            print'a non-valid message has been received from commands exchange , info:\n {0}'.format(body)

        if body['command'] == 'close':
            exit()

def start():
    print "Player is waiting for messages from actions and commands exchanges ....."
    # Create exchanges and queues to aply at connection
    exchange = Exchange(actions_exchange, type="topic", durable=False)  # actions exchange
    exchange2 = Exchange(commands_exchange, type="topic", durable=False)         # commands exchange
    queues = [Queue(actions_queue_name, exchange, routing_key=actions_binding_key, durable=False, exclusive=False), Queue(commands_queue_name, exchange2, routing_key=commands_binding_key, durable=False, exclusive=False)]

    with Connection(hostname=rabbit_ip, port=5672, userid=rabbit_user, password=rabbit_passw, virtual_host=rabbit_vhost, heartbeat=4) as conn:
        worker = Worker(conn, queues)
        worker.run()

def main(argv):
    argp = ArgumentParser(version='1.0', description='video flow player', epilog='Pablo Salva Garcia (UWS)')
    argp.add_argument('--start', action="store_true", help='The player client will start to consume messages from actinos and commands exchanges')

    arguments = argp.parse_args()
    # (--start) Starts player consumer
    if arguments.start:
        start()

if __name__ == "__main__":
    main(sys.argv[1:])
