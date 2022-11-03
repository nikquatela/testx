# -*- coding: utf-8 -*-

# from plone import api
from csi.concorsi import _
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class RapportoConcorso(object):
    proxyfield = None

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = []
        items.append(VocabItem('determinato', _('Subordinato a tempo determinato')))
        items.append(VocabItem('indeterminato', _('Subordinato a tempo indeterminato')))
        items.append(VocabItem('cococo', _('Contratto di lavoro autonomo')))

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
class RapportoConcorsoRicercatore(object):
    proxyfield = None

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = []
        items.append(VocabItem('ricercatore', _('Ricercatore')))
        items.append(VocabItem('associato', _('Associato')))

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
class GetRapportoConcorso(RapportoConcorso):
    """
    """
    proxyfield = 'rapporto'

RapportoConcorsoFactory = GetRapportoConcorso()


@implementer(IVocabularyFactory)
class GetRapportoConcorsoRicercatore(RapportoConcorsoRicercatore):
    """
    """
    proxyfield = 'rapporto'

RapportoConcorsoRicercatoreFactory = GetRapportoConcorsoRicercatore()
