# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.api import FacebookAdsApi

access_token = '<ACCESS_TOKEN>'
app_secret = '<APP_SECRET>'
app_id = '<APP_ID>'
id = '<AD_CREATIVE_ID>'
FacebookAdsApi.init(access_token=access_token)

fields = [
  'name',
  'object_story_id',
]
params = {
}
print AdCreative(id).get(
  fields=fields,
  params=params,
)