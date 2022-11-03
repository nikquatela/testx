# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from csi.concorsi import _
from csi.concorsi.tableschema import IMyRowSchema
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from z3c.relationfield.schema import RelationChoice
from zope import schema

from Products.CMFPlone.utils import safe_unicode


class IAdesione(model.Schema):
    """ Marker interface and Dexterity Python Schema for Adesione
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    """ model.load('adesione.xml') """

    """ title = schema.TextLine(
        title=_(u'label_title', default=u'Title'),
        required=False,
    )
    description = schema.Text(
        title=_(u'label_description', default=u'Summary'),
        required=False,
    )
    directives.omitted('description')
    directives.omitted('title') """

    corso = RelationChoice(
        title=_(u'Accedi alla scheda del corso'),
        description=_(u'Cliccare su Aggiungi e selezionare il corso per cui si vuole fornire una lista di studenti'),
        source=CatalogSource(
            {
                "portal_type": ["Corso"],
                "review_state": "published",
            }
        ),
        required=False,
    )
    directives.widget(
        'corso',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['Corso'],
            'basePath': '/Plone/corsi',
        },
    )

    studenti = schema.List(
        title=_(u'Studenti proposti'),
        description=_(u"Fornire l'elenco ordinato di studenti proposti per il corso"),
        value_type=DictRow(title=u'Table', schema=IMyRowSchema),
        default=[],
        required=False,
    )
    directives.widget('studenti', DataGridFieldFactory)

@implementer(IAdesione)
class Adesione(Container):
    """ Content-type class for IAdesione
    """

    @property
    def title(self):
        if self.corso is None:
            return ''
        corso = self.corso
        title = corso.title
        return (u'Richiesta di adesione a: %s' % safe_unicode(title)).encode('utf8', errors='xmlcharrefreplace')
    
    @title.setter
    def title(self,value):
        pass

    """ DA CONTROLLARE """
    
   