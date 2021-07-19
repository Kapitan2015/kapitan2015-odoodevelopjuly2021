# See LICENSE file for full copyright and licensing details.

import urllib
import simplejson
from odoo.http import request
from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)
class AuthOauthProvider(models.Model):
    """Class defining the configuration values of an OAuth2 provider"""

    _inherit = 'auth.oauth.provider'

    secret_key = fields.Char('Secret Key')

    def oauth_token(
            self, type_grant, oauth_provider_rec, code=None,
            refresh_token=None, context=None):
        data = dict(
            grant_type=type_grant,
            redirect_uri=request.env['ir.config_parameter'].sudo().get_param(
                'web.base.url2') + '/auth_oauth/microsoft/signin',
            client_id=oauth_provider_rec.client_id,
            response_mode='form_post',
            client_secret=oauth_provider_rec.secret_key,
            scope='openid'
        )
        _logger.info("oauth_provider_rec.validation_endpoint " + str(oauth_provider_rec.validation_endpoint))
        if code:
            data.update({'code': code})
        elif refresh_token:
            data.update({'refresh_token': refresh_token})
        _logger.info("oauth_provider_rec.data " + str(data))
        return simplejson.loads(urllib.request.urlopen(
            urllib.request.Request(
                oauth_provider_rec.validation_endpoint,
                urllib.parse.urlencode(data).encode("utf-8"))).read())
