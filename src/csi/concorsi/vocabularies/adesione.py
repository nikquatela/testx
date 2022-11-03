# -*- coding: utf-8 -*-

# from plone import api
from csi.concorsi import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value

@implementer(IVocabularyFactory)
class ClassiAmmesse(object):
    proxyfield = None

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = []
        items.append(VocabItem('', _('-')))
        items.append(VocabItem('4', _('IV')))
        items.append(VocabItem('5', _('V')))

        # create a list of SimpleTerm items:
        terms = []
        for item in items:
            terms.append(
                SimpleTerm(
                    value=item.token,
                    token=str(item.token),
                    title=item.value,
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class GetClassi(ClassiAmmesse):
    """
    """
    proxyfield = 'classe'

ClassiFactory = GetClassi()