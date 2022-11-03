# -*- coding: utf-8 -*-

# from plone import api
#from csi.concorsi.vocabularies import defaultListTest
from plone.app.vocabularies.catalog import KeywordsVocabulary
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory


#from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

""" class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value """

@implementer(IVocabularyFactory)
class GetListaProve(KeywordsVocabulary):
    keyword_index = 'prove'
    path_index = 'path'

    """ def __call__(self, context):
        items = []

        for item in defaultListTest():
            item = item.strip()
            if not item:
                continue
            items.append(VocabItem(item, item))

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
        return SimpleVocabulary(terms) """

ListaProveFactory = GetListaProve()


@implementer(IVocabularyFactory)
class GetListaStrutture(KeywordsVocabulary):
    keyword_index = 'struttura'
    path_index = 'path'

ListaStruttureFactory = GetListaStrutture()


@implementer(IVocabularyFactory)
class GetCategorieStrutture(KeywordsVocabulary):
    keyword_index = 'categoria'
    path_index = 'path'

ListaCategorieFactory = GetCategorieStrutture()


@implementer(IVocabularyFactory)
class GetListaAree(KeywordsVocabulary):
    keyword_index = 'area'
    path_index = 'path'

ListaAreeFactory = GetListaAree()


""" @implementer(IVocabularyFactory)
class GetListaCommissione(KeywordsVocabulary):
    keyword_index = 'componenti_commissione'
    path_index = 'path'

ListaCommissioneFactory = GetListaCommissione() """
