##############################################################################
# Start zope with twisted WSGI server
#
# Install required python packages with pip:
#
#     ./venv/bin/pip install twisted plaster plaster_pastedeploy
#
# Start zope:
#
#     ./venv/bin/twistd -ny shop.tac
##############################################################################

# use asyncio main loop in twisted
from twisted.internet import asyncioreactor
asyncioreactor.install()

from twisted.application import internet
from twisted.application import service
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
import os
import plaster

config='./instance/etc/zope.ini'
config = os.path.abspath(config)
port = 8081

# Get the WSGI application
loader = plaster.get_loader(config, protocols=['wsgi'])
app = loader.get_wsgi_app('main')

# Twisted WSGI server setup
resource = WSGIResource(reactor, reactor.getThreadPool(), app)
factory = Site(resource)

# Twisted Application setup
application = service.Application('zope')
internet.TCPServer(port, factory).setServiceParent(application)
