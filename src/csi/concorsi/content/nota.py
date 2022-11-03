# -*- coding: utf-8 -*-
from plone.app.dexterity.behaviors.metadata import _ as _p
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.form.interfaces import IAddForm, IEditForm
from zope import schema
from zope.interface import implementer


# from csi.concorsi import _


class INota(model.Schema):
    """ Marker interface and Dexterity Python Schema for Nota
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    #model.load('nota.xml')

    title = schema.TextLine(
        title=_p(u'label_title', default=u'Title'),
        required=True,
    )

    contenuto_nota = RichText(
         title=_p(u'Contenuto della nota'),
         required=True
     )

    directives.order_before(contenuto_nota='*')
    directives.order_before(title='*')
    directives.no_omit(IAddForm, 'title','contenuto_nota')
    directives.no_omit(IEditForm, 'title','contenuto_nota')


@implementer(INota)
class Nota(Item):
    """ Content-type class for INota
    """
