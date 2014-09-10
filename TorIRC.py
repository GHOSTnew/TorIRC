#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyleft 2013 GHOSTnew
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socks
import socket
import ssl
import time
from threading import Thread


class LocalIRC(object):

    def __init__(self):
        self.lsock = socket.socket()
        self.buffer = ''
        self.client_ok = None
        self.nick = None

    def connect(self):
        self.lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lsock.bind(('127.0.0.1', 20000))
        self.lsock.listen(5)
        self.client_ok, client_info = self.lsock.accept()

    def recv(self):
        while True:
            block = self.client_ok.recv(1024)
            if not block:
                break
            self.buffer += block
            while self.buffer.find('\n') != -1:
                line, self.buffer = self.buffer.split('\n', 1)
                server.send(line)
                print "client: " + line
                if line.find('QUIT') != -1:
                    self.lsock.close()
                    server.die()
                    break
                elif line.find('NICK') != -1:
                    arg = line.split(" ")
                    if len(arg) <= 2:
                        self.nick = arg[1]
                        print self.nick

    def send(self, msg):
        self.client_ok.send(msg + '\n')

    def notice(self, msg):
        if self.nick:
            self.send(':Info!TOR@TorIRC NOTICE ' + self.nick + ' :' + msg)


class TorIRC(object):
    def __init__(self, host, port, ssl=False):
        self.host = host
        self.port = port
        self.ssl = ssl

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
        socket.socket = socks.socksocket

        self.tsock = socket.socket()
        self.buffer = ''

        self.last_ping = 0

    def connect(self):
        self.tsock.connect((self.host, self.port))
        if self.ssl is True:
            try:
                self.tsock = ssl.wrap_socket(self.tsock)
                self.tsock.do_handshake()
            except:
                client.notice("\002[\0034-\003] Failed to do ssl handshake")

    def recv(self):
        while True:
            block = self.tsock.recv(1024)
            if not block:
                break
            self.buffer += block
            while self.buffer.find('\n') != -1:
                line, self.buffer = self.buffer.split('\n', 1)
                if line.find('PRIVMSG') != -1:
                    message = ':'.join(line.split(':')[2:])
                    msg = message.split()[0]
                    if msg.startswith("\001") & msg.endswith("\001"):
                        client.notice("\002[\0034-\003] CTCP reçu mais rejeté par sécurité")
                    else:
                        client.send(line)
                elif line.find('PONG') != -1:
                    self.last_ping = int(time.time())
                    client.send(line)
                else:
                    client.send(line)
                print "server: " + line

    def send(self, msg):
        self.tsock.send(msg + '\r\n')

    def ping_time_out(self):
        while True:
            now = int(time.time())
            if now - self.last_ping > 60*4:
                client.send("QUIT :ping time out")
                break
            time.sleep(2)

    def die(self):
        self.tsock.close()

if __name__ == "__main__":
    print "== TorIRC =="
    print "Lancement du serveur local"
    client = LocalIRC()
    print "Le serveur est maintenant ouvert sur 127.0.0.1 port 20000"
    client.connect()
    server = TorIRC("oghzthm3fgvkh5wo.onion", 6697, True)
    server.connect()
    Thread(target=client.recv).start()
    Thread(target=server.recv).start()
    Thread(target=server.ping_time_out).start()
