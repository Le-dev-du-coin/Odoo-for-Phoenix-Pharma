from odoo import http
from odoo.http import request


class TestController(http.Controller):

    @http.route('/page_test', type='http', auth='user', website=True)
    def page_test(self, **kw):
        return request.render('test_fetch.test_template')

    @http.route('/test/api', type='json', auth='user', methods=['GET'] ,website=True)
    def testForFetch(self , search=None, **kw):
        if not search:
            return('Non touver')
        response = {
            'Response': 'OK',
            'search': search
        }
        return response