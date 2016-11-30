#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title           :miscron.py
# description     : Runs commands to a server
# author          :Chris Sprance / Entrada Interactive
# usage           : This script is CLI for server administaration to run it from a command line do:
# misrcon.py -i [ip] --port [admin port] -p [admin password] --command [command] --time [exec_time] --s [schedule]
# python_version  :2.7.5
# ==============================================================================
import xmlrpclib
import hashlib
import argparse
from datetime import datetime
from datetime import timedelta
from threading import Timer
from gooey import Gooey


class SpecialTransport(xmlrpclib.Transport):
    user_agent = 'MisRCON-Apollo'

    def send_content(self, connection, request_body):
        connection.putheader("Connection", "keep-alive")
        connection.putheader("Content-Type", "text/xml")
        connection.putheader("Content-Length", str(len(request_body)))
        connection.endheaders()
        if request_body:
            connection.send(request_body)


def add_one_day_to_time(t):
    hour, minute = t.split(':')
    x = datetime.today()
    y = (x + timedelta(days=1)).replace(hour=int(hour), minute=int(minute), second=0)
    return y


def schedule_run(server_url, password, cmdstring, exec_time):
    """
    Schedules an rcon to run the next day at a specific time then starts a new timer when it runs
    :param server_url: http://192.168.1.1:9999/rpc2 string
    :param password: the server http password: 123456
    :param cmdstring: string that contains the command and any params mis_kick player
    :param exec_time: the time to schedule the run at 14:33
    :return:
    """
    hour, minute = exec_time.split(':')

    x = datetime.today()
    y = (x + timedelta(days=1)).replace(hour=int(hour), minute=int(minute), second=0)
    delta_t = y - x

    secs = delta_t.seconds + 1

    def hello_world():
        send_rcon(server_url, password, cmdstring, exec_time)

    t = Timer(secs, hello_world)
    t.start()
    print "Waiting to run again, do not close this window...."


# noinspection PyTypeChecker
def send_rcon(server_url, password, cmdstring, exec_time=False, schedule_only=False):
    '''
    Authenticate and send the xml-rpc command and
    then print the command string that's returned
    :param server_url: http://192.168.1.1:9999/rpc2 string
    :param password: the server http password: 123456
    :param cmdstring: string that contains the command and any params mis_kick player
    :param exec_time: the time to schedule the run at 14:33
    :param schedule_only: whether or not we schedule and run or only schedule
    :return: a failure message from the server on authentication failed or response on success
    """
    '''
    if exec_time:
        print "This command will run again at: " + str(add_one_day_to_time(exec_time))
        schedule_run(server_url, password, cmdstring, exec_time)
    if schedule_only is False:
        cmd_list = cmdstring.split(' ')
        cmd = cmd_list.pop(0)  # first thing sent is always a command
        # we popped out the 0 before so the rest are params
        params = ' '.join(cmd_list) if len(cmd_list) > 0 else ''
        # start the connection
        server = xmlrpclib.ServerProxy(
            server_url, transport=SpecialTransport(), allow_none=True)
        # authenticate with the uptime and the password md5d with : between
        md5 = hashlib.md5(server.challenge() + ':' + password).hexdigest()
        if len(params) > 0:
            return server.__getattr__(cmd)(params) if server.authenticate(
                md5) == 'authorized' else 'Authentication Failed......'
        else:
            return server.__getattr__(cmd)() if server.authenticate(
                md5) == 'authorized' else 'Authentication Failed......'


@Gooey
def main():
    parser = argparse.ArgumentParser('MisRCON - Server RCON CLI for Miscreated')
    parser.add_argument('-i', '--ip', type=str, required=True,
                        help="IP address of server")
    parser.add_argument('-P', '--port', type=str, required=True,
                        help="Admin port of server")
    parser.add_argument('-p', '--password', type=str, required=True,
                        help="Admin password of server")
    parser.add_argument('-c', '--command', type=str, required=True,
                        help="Command string to send sv_say Server shutting down in 5 minutes")
    parser.add_argument('-t', '--time', type=str, required=False,
                        help="The time you want to run the command again. This will always be 1 day ahead. ex: 16:45")
    parser.add_argument('-s', '--schedule_only', required=False, action='store_true',
                        help="Should we only schedule or schedule and run it.")
    args = parser.parse_args()
    ip = args.ip
    # port = str(int(get['port'].value) + 4)
    # workaround for no server panel from i3d
    port = args.port
    password = args.password
    command = args.command
    exec_time = args.time if args.time is not None else False
    schedule_only = args.schedule_only if args.schedule_only is not None else False
    server_url = 'http://%s:%s/rpc2' % (ip, port)
    result = send_rcon(server_url, password, command, exec_time, schedule_only)
    if result is not None:
        print result


if __name__ == '__main__':
    main()
