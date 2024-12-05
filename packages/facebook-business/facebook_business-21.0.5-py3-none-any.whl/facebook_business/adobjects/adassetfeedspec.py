# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from facebook_business.adobjects.abstractobject import AbstractObject

"""
This class is auto-generated.

For any issues or feature requests related to this class, please let us know on
github and we'll fix in our codegen framework. We'll not be able to accept
pull request for this class.
"""

class AdAssetFeedSpec(
    AbstractObject,
):

    def __init__(self, api=None):
        super(AdAssetFeedSpec, self).__init__()
        self._isAdAssetFeedSpec = True
        self._api = api

    class Field(AbstractObject.Field):
        ad_formats = 'ad_formats'
        additional_data = 'additional_data'
        app_product_page_id = 'app_product_page_id'
        asset_customization_rules = 'asset_customization_rules'
        autotranslate = 'autotranslate'
        bodies = 'bodies'
        call_ads_configuration = 'call_ads_configuration'
        call_to_action_types = 'call_to_action_types'
        call_to_actions = 'call_to_actions'
        captions = 'captions'
        carousels = 'carousels'
        descriptions = 'descriptions'
        events = 'events'
        groups = 'groups'
        images = 'images'
        link_urls = 'link_urls'
        message_extensions = 'message_extensions'
        onsite_destinations = 'onsite_destinations'
        optimization_type = 'optimization_type'
        promotional_metadata = 'promotional_metadata'
        reasons_to_shop = 'reasons_to_shop'
        shops_bundle = 'shops_bundle'
        titles = 'titles'
        upcoming_events = 'upcoming_events'
        videos = 'videos'

    class CallToActionTypes:
        add_to_cart = 'ADD_TO_CART'
        apply_now = 'APPLY_NOW'
        ask_about_services = 'ASK_ABOUT_SERVICES'
        ask_for_more_info = 'ASK_FOR_MORE_INFO'
        audio_call = 'AUDIO_CALL'
        book_a_consultation = 'BOOK_A_CONSULTATION'
        book_now = 'BOOK_NOW'
        book_travel = 'BOOK_TRAVEL'
        buy = 'BUY'
        buy_now = 'BUY_NOW'
        buy_tickets = 'BUY_TICKETS'
        buy_via_message = 'BUY_VIA_MESSAGE'
        call = 'CALL'
        call_me = 'CALL_ME'
        call_now = 'CALL_NOW'
        chat_with_us = 'CHAT_WITH_US'
        confirm = 'CONFIRM'
        contact = 'CONTACT'
        contact_us = 'CONTACT_US'
        donate = 'DONATE'
        donate_now = 'DONATE_NOW'
        download = 'DOWNLOAD'
        event_rsvp = 'EVENT_RSVP'
        find_a_group = 'FIND_A_GROUP'
        find_your_groups = 'FIND_YOUR_GROUPS'
        follow_news_storyline = 'FOLLOW_NEWS_STORYLINE'
        follow_page = 'FOLLOW_PAGE'
        follow_user = 'FOLLOW_USER'
        get_a_quote = 'GET_A_QUOTE'
        get_directions = 'GET_DIRECTIONS'
        get_offer = 'GET_OFFER'
        get_offer_view = 'GET_OFFER_VIEW'
        get_promotions = 'GET_PROMOTIONS'
        get_quote = 'GET_QUOTE'
        get_showtimes = 'GET_SHOWTIMES'
        get_started = 'GET_STARTED'
        inquire_now = 'INQUIRE_NOW'
        install_app = 'INSTALL_APP'
        install_mobile_app = 'INSTALL_MOBILE_APP'
        join_channel = 'JOIN_CHANNEL'
        learn_more = 'LEARN_MORE'
        like_page = 'LIKE_PAGE'
        listen_music = 'LISTEN_MUSIC'
        listen_now = 'LISTEN_NOW'
        make_an_appointment = 'MAKE_AN_APPOINTMENT'
        message_page = 'MESSAGE_PAGE'
        mobile_download = 'MOBILE_DOWNLOAD'
        no_button = 'NO_BUTTON'
        open_instant_app = 'OPEN_INSTANT_APP'
        open_link = 'OPEN_LINK'
        order_now = 'ORDER_NOW'
        pay_to_access = 'PAY_TO_ACCESS'
        play_game = 'PLAY_GAME'
        play_game_on_facebook = 'PLAY_GAME_ON_FACEBOOK'
        purchase_gift_cards = 'PURCHASE_GIFT_CARDS'
        raise_money = 'RAISE_MONEY'
        record_now = 'RECORD_NOW'
        refer_friends = 'REFER_FRIENDS'
        request_time = 'REQUEST_TIME'
        say_thanks = 'SAY_THANKS'
        see_more = 'SEE_MORE'
        sell_now = 'SELL_NOW'
        send_a_gift = 'SEND_A_GIFT'
        send_gift_money = 'SEND_GIFT_MONEY'
        send_updates = 'SEND_UPDATES'
        share = 'SHARE'
        shop_now = 'SHOP_NOW'
        sign_up = 'SIGN_UP'
        sotto_subscribe = 'SOTTO_SUBSCRIBE'
        start_order = 'START_ORDER'
        subscribe = 'SUBSCRIBE'
        swipe_up_product = 'SWIPE_UP_PRODUCT'
        swipe_up_shop = 'SWIPE_UP_SHOP'
        update_app = 'UPDATE_APP'
        use_app = 'USE_APP'
        use_mobile_app = 'USE_MOBILE_APP'
        video_annotation = 'VIDEO_ANNOTATION'
        video_call = 'VIDEO_CALL'
        view_channel = 'VIEW_CHANNEL'
        view_product = 'VIEW_PRODUCT'
        visit_pages_feed = 'VISIT_PAGES_FEED'
        watch_more = 'WATCH_MORE'
        watch_video = 'WATCH_VIDEO'
        whatsapp_message = 'WHATSAPP_MESSAGE'
        woodhenge_support = 'WOODHENGE_SUPPORT'

    _field_types = {
        'ad_formats': 'list<string>',
        'additional_data': 'AdAssetFeedAdditionalData',
        'app_product_page_id': 'string',
        'asset_customization_rules': 'list<AdAssetFeedSpecAssetCustomizationRule>',
        'autotranslate': 'list<string>',
        'bodies': 'list<AdAssetFeedSpecBody>',
        'call_ads_configuration': 'Object',
        'call_to_action_types': 'list<CallToActionTypes>',
        'call_to_actions': 'list<AdAssetFeedSpecCallToAction>',
        'captions': 'list<AdAssetFeedSpecCaption>',
        'carousels': 'list<AdAssetFeedSpecCarousel>',
        'descriptions': 'list<AdAssetFeedSpecDescription>',
        'events': 'list<AdAssetFeedSpecEvents>',
        'groups': 'list<AdAssetFeedSpecGroupRule>',
        'images': 'list<AdAssetFeedSpecImage>',
        'link_urls': 'list<AdAssetFeedSpecLinkURL>',
        'message_extensions': 'list<AdAssetMessageExtensions>',
        'onsite_destinations': 'list<AdAssetOnsiteDestinations>',
        'optimization_type': 'string',
        'promotional_metadata': 'Object',
        'reasons_to_shop': 'bool',
        'shops_bundle': 'bool',
        'titles': 'list<AdAssetFeedSpecTitle>',
        'upcoming_events': 'list<Object>',
        'videos': 'list<AdAssetFeedSpecVideo>',
    }
    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        field_enum_info['CallToActionTypes'] = AdAssetFeedSpec.CallToActionTypes.__dict__.values()
        return field_enum_info


