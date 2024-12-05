# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.lead import Lead
from facebook_business.api import FacebookAdsApi

access_token = '<ACCESS_TOKEN>'
app_secret = '<APP_SECRET>'
app_id = '<APP_ID>'
id = '<AD_GROUP_ID>'
FacebookAdsApi.init(access_token=access_token)

fields = [
]
params = {
  'filtering': [{'field':'time_created','operator':'GREATER_THAN','value':1721709809}],
}
print Ad(id).get_leads(
  fields=fields,
  params=params,
)