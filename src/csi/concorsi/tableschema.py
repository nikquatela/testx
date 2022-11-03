# -*- coding: utf-8 -*-
from csi.concorsi import _
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.schema.email import Email
from zope import schema
from zope.interface import Interface


class IMyRowSchema(Interface):

    nome = schema.TextLine(
        title=_(u"Nome"),
        required=False,
        )
    cognome = schema.TextLine(
        title=_(u"Cognome"),
        required=False,
        )
    data_nascita = schema.TextLine(
        title=_(u"Data di nascita"),
        required=False,
        )

    classe = schema.Choice(
        title=_(u"Classe"),
        vocabulary='csi.concorsi.classi',
        required=False,
        )
    directives.widget('classe', SelectFieldWidget)

    sezione = schema.TextLine(
        title=_(u"Sezione"),
        required=False,
        )

    email = Email(
        title=u'Email',
        required=False,
        )
