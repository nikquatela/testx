# -*- coding: utf-8 -*-

# from plone import api
from plone.app.vocabularies.catalog import KeywordsVocabulary
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory


@implementer(IVocabularyFactory)
class GetListaStrutture(KeywordsVocabulary):
    keyword_index = 'struttura'
    path_index = 'path'


ListaStruttureFactory = GetListaStrutture()
