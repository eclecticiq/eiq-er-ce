import json

from flask import request, send_file
from flask_restplus import Namespace, Resource, marshal

from .utils import *
from polylogyx.utils import require_api_key
from polylogyx.dao import carves_dao as dao
from polylogyx.dao import nodes_dao as nodedao
from polylogyx.wrappers import parent_wrappers as parentwrapper
from polylogyx.wrappers import carve_wrappers as wrapper
from polylogyx.constants import PolyLogyxServerDefaults

ns = Namespace('carves', description='Carves related operations')


@require_api_key
@ns.route('/', endpoint='node_carves_list')
@ns.doc(params={'host_identifier': 'Host identifier of the Node'})
class NodeCarvesList(Resource):
    '''lists out the carves for a specific node when host_identifier given otherwise returns all carves'''
    parser = requestparse(['host_identifier'],[str],["host identifier of the node"])

    @ns.expect(parser)
    def post(self):
        carves = None
        status = 'success'
        host_identifier = self.parser.parse_args()['host_identifier']

        if host_identifier:
            node = nodedao.get_node_by_host_identifier(host_identifier)
            if not node:
                status = 'failure'
                message = 'Node with this identifier does not exist'
            else:
                carves = dao.get_carves_by_node_id(node.id)
                carves = marshal(carves, wrapper.carves_wrapper)
                message = 'Successfully fetched the carves'
        else:
            carves = dao.get_carves_all()
            carves = marshal(carves, wrapper.carves_wrapper)
            message = 'Successfully fetched the carves'
        if not carves: message = "carves data doesn't exists for the input given"
        return marshal(respcls(message,status,carves),parentwrapper.common_response_wrapper)


@require_api_key
@ns.route('/download/<string:session_id>', endpoint='download_carves')
@ns.doc(params={'session_id': 'session id'})
class DownloadCarves(Resource):
    '''download carves through session id'''

    def get(self, session_id):
        status = 'failure'
        message = 'Data missing'
        if not session_id:
            message = 'Please provide a session id'
        else:
            carve_session = dao.get_carves_by_session_id(session_id)
            if carve_session:
                status = 'success'
                message = 'Successfully fetched the carves'
                print ('file is : '+PolyLogyxServerDefaults.BASE_URL + '/carves/' + carve_session.node.host_identifier + '/'+carve_session.archive)
                data = send_file(PolyLogyxServerDefaults.BASE_URL + '/carves/' + carve_session.node.host_identifier + '/'+ carve_session.archive , as_attachment=True, attachment_filename='carve_session.archive')
                return data
            else:
                message = 'This session id does not exist'

        return marshal(respcls(message,status), parentwrapper.common_response_wrapper, skip_none=True)