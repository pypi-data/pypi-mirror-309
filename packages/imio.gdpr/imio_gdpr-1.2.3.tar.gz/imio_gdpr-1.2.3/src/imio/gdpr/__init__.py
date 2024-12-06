# -*- coding: utf-8 -*-
"""Init and utils."""
from six import text_type
from plone import api
from Products.PortalTransforms.libtransforms.utils import bodyfinder
from zope.i18nmessageid import MessageFactory
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


_ = MessageFactory("imio.gdpr")

HAS_PLONE_5_AND_MORE = api.env.plone_version().startswith(
    "5"
) or api.env.plone_version().startswith("6")

DEFAULT_GDPR_FILES = [
    "gdpr-explanation",
    "mentions-legales",
    "mentions-legales-nl",
    "mentions-legales-en",
    "mentions-legales-de",
]

DEFAULT_COOKIES_FILES = [
    "cookies-policy",
    "cookies-policy-nl",
    "cookies-policy-en",
    "cookies-policy-de",
]


def get_text_from_view(view_name):
    """
    Text get from a browser view template <body> tag
    """
    portal = api.portal.get()
    request = getattr(portal, "REQUEST", None)
    if request is not None:
        view = api.content.get_view(name=view_name, context=portal, request=request)
        if view is not None:
            text = bodyfinder(view.index()).strip()
            if not isinstance(text, text_type):
                text = text.decode("utf-8")
            return text
    return ""


@provider(IContextAwareDefaultFactory)
def get_default_text(context):
    return get_text_from_view("default_gdpr_text")


@provider(IContextAwareDefaultFactory)
def get_default_cookies_text(context):
    return get_text_from_view("default_cookies_text")
