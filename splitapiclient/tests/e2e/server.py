from __future__ import absolute_import, division, print_function, \
    unicode_literals
import tornado.ioloop
import tornado.web
from backend.handlers import EnvironmentsHandler, IdentityHandler, \
    MultiIdentityHandler, TrafficTypeAttributesHandler, TrafficTypesHandler


def make_app():
    return tornado.web.Application([
        (r'/trafficTypes/(\w+)/schema/(\w+)', TrafficTypeAttributesHandler),
        (r'/trafficTypes/(\w+)/schema', TrafficTypeAttributesHandler),
        (r'/trafficTypes/(\w+)/environments/(\w+)/identities/(\w+)/patch',
         IdentityHandler),
        (r'/trafficTypes/(\w+)/environments/(\w+)/identities/(\w+)',
         IdentityHandler),
        (r'/trafficTypes/(\w+)/environments/(\w+)/identities',
         MultiIdentityHandler),
        (r'/trafficTypes', TrafficTypesHandler),
        (r'/environments', EnvironmentsHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
