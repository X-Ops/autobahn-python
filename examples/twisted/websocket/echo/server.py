###############################################################################
##
##  Copyright (C) 2011-2013 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory
from autobahn.websocket import http


#from twisted.internet.defer import Deferred
from twisted.internet.defer import Deferred, returnValue, inlineCallbacks
from twisted.internet import reactor


def inlinesleep(delay):
   d = Deferred()
   def resume():
      d.callback(None)
   reactor.callLater(delay, resume)
   return d


class MyServerProtocol(WebSocketServerProtocol):

   @inlineCallbacks
   def myfun(self):
      r = yield inlinesleep(0.8)
      returnValue(r)

   @inlineCallbacks
   def onConnect(self, request):
      yield inlinesleep(0.8)
      #return self.myfun()
      #res = yield self.myfun()
      #returnValue(res)

   @inlineCallbacks
   def onConnect2(self, request):
      print("Client connecting: {}".format(request.peer))
      d = Deferred()
      def fail():
         #raise Exception("denied")
         #raise http.HttpException(http.UNAUTHORIZED[0], "You are now allowed.")
         #d.errback(http.HttpException(http.UNAUTHORIZED[0], "You are now allowed."))
         #d.errback(Exception("denied"))
         d.callback(None)
      self.factory.reactor.callLater(0.2, fail)
      return d

   def onOpen(self):
      print("WebSocket connection open.")

   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {} bytes".format(len(payload)))
      else:
         print("Text message received: {}".format(payload.decode('utf8')))

      ## echo back message verbatim
      self.sendMessage(payload, isBinary)

   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {}".format(reason))



if __name__ == '__main__':

   import sys

   from twisted.python import log
   from twisted.internet import reactor

   log.startLogging(sys.stdout)

   factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
   factory.protocol = MyServerProtocol

   reactor.listenTCP(9000, factory)
   reactor.run()   
