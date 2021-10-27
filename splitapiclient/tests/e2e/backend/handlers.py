import json
import tornado.web
import tornado.escape
from backend import responses


class BaseHandler(tornado.web.RequestHandler):
    def auth(self):
        if not self.request.headers.get('Authorization') == 'Bearer Admin':
            self.set_status(401)
            self.finish()
            return False
        return True


class TrafficTypesHandler(BaseHandler):
    def get(self):
        if self.auth():
            self.write(json.dumps(responses.traffic_types_all))


class EnvironmentsHandler(BaseHandler):
    def get(self):
        self.write(json.dumps(responses.environments_all))

class WorkspacesHandler(BaseHandler):
    def get(self):
        self.write(json.dumps(responses.workspaces_all))


class TrafficTypeAttributesHandler(BaseHandler):
    def get(self, traffic_type_id):
        attrs = responses.traffic_type_attributes.get(traffic_type_id)
        if attrs:
            self.write(json.dumps(attrs))
        else:
            self.clear()
            self.set_status(404)
            self.finish()

    def put(self, traffic_type_id):
        '''
        '''
        jbody = tornado.escape.json_decode(self.request.body)
        # TODO: Validate jbody
        attrs = responses.traffic_type_attributes.get(traffic_type_id)
        if attrs:
            attrs.append(jbody)
            self.write(json.dumps(jbody))
        else:
            self.set_status(404)
            self.finish()

    def delete(self, traffic_type_id, attribute_id):
        '''
        '''
        try:
            all_attrs = responses.traffic_type_attributes[traffic_type_id]
            attr = next(a for a in all_attrs if a['id'] == attribute_id)
            if attr is not None:
                all_attrs.remove(attr)
            self.set_status(200)
            self.finish()
        except:
            import traceback
            traceback.print_exc()
            self.set_status(500)
            self.finish()


class IdentityHandler(BaseHandler):
    '''
    '''
    def put(self, traffic_type_id, environment_id, key):
        '''
        '''
        jbody = tornado.escape.json_decode(self.request.body)
        if key != jbody['key']:
            self.set_status(400)
            self.finish()
        else:
            self.write(json.dumps(jbody))
            self.finish()

    def post(self, traffic_type_id, environment_id, key):
        '''
        '''
        jbody = tornado.escape.json_decode(self.request.body)
        if key != jbody['key']:
            self.set_status(400)
            self.finish()
        else:
            self.write(json.dumps(jbody))
            self.finish()

    def patch(self, traffic_type_id, environment_id, key):
        '''
        '''
        jbody = tornado.escape.json_decode(self.request.body)
        if key != jbody['key']:
            self.set_status(400)
            self.finish()
        else:
            self.write(json.dumps(jbody))
            self.finish()

    def delete(self, traffic_type_id, environment_id, key):
        '''
        '''
        self.set_status(200)
        self.finish()


class MultiIdentityHandler(BaseHandler):
    '''
    '''
    def post(self, traffic_type_id, environment_id):
        '''
        '''
        jbody = tornado.escape.json_decode(self.request.body)
        self.write(json.dumps({
            'objects': jbody,
            'failed': [],
            'metadata': {},
        }))
        self.finish()
