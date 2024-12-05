# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from facebook_business.adobjects.abstractobject import AbstractObject
from facebook_business.adobjects.abstractcrudobject import AbstractCrudObject
from facebook_business.adobjects.objectparser import ObjectParser
from facebook_business.api import FacebookRequest
from facebook_business.typechecker import TypeChecker

"""
This class is auto-generated.

For any issues or feature requests related to this class, please let us know on
github and we'll fix in our codegen framework. We'll not be able to accept
pull request for this class.
"""

class AdsReportBuilderExportCore(
    AbstractCrudObject,
):

    def __init__(self, fbid=None, parent_id=None, api=None):
        self._isAdsReportBuilderExportCore = True
        super(AdsReportBuilderExportCore, self).__init__(fbid, parent_id, api)

    class Field(AbstractObject.Field):
        async_percent_completion = 'async_percent_completion'
        async_report_url = 'async_report_url'
        async_status = 'async_status'
        client_creation_value = 'client_creation_value'
        expiry_time = 'expiry_time'
        export_download_time = 'export_download_time'
        export_format = 'export_format'
        export_name = 'export_name'
        export_type = 'export_type'
        has_seen = 'has_seen'
        id = 'id'
        is_sharing = 'is_sharing'
        link_sharing_expiration_time = 'link_sharing_expiration_time'
        link_sharing_uri = 'link_sharing_uri'
        time_completed = 'time_completed'
        time_start = 'time_start'

    def api_get(self, fields=None, params=None, batch=None, success=None, failure=None, pending=False):
        from facebook_business.utils import api_utils
        if batch is None and (success is not None or failure is not None):
          api_utils.warning('`success` and `failure` callback only work for batch call.')
        param_types = {
        }
        enums = {
        }
        request = FacebookRequest(
            node_id=self['id'],
            method='GET',
            endpoint='/',
            api=self._api,
            param_checker=TypeChecker(param_types, enums),
            target_class=AdsReportBuilderExportCore,
            api_type='NODE',
            response_parser=ObjectParser(reuse_object=self),
        )
        request.add_params(params)
        request.add_fields(fields)

        if batch is not None:
            request.add_to_batch(batch, success=success, failure=failure)
            return request
        elif pending:
            return request
        else:
            self.assure_call()
            return request.execute()

    _field_types = {
        'async_percent_completion': 'int',
        'async_report_url': 'string',
        'async_status': 'string',
        'client_creation_value': 'string',
        'expiry_time': 'datetime',
        'export_download_time': 'datetime',
        'export_format': 'string',
        'export_name': 'string',
        'export_type': 'string',
        'has_seen': 'bool',
        'id': 'string',
        'is_sharing': 'bool',
        'link_sharing_expiration_time': 'datetime',
        'link_sharing_uri': 'string',
        'time_completed': 'datetime',
        'time_start': 'datetime',
    }
    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        return field_enum_info


