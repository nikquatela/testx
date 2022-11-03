# -*- coding: utf-8 -*-
from csi.concorsi import _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer
from zope import schema
from plone.schema.email import Email
from collective import dexteritytextindexer




class IScuola(model.Schema):
    """ Marker interface for Scuola
    """

    """ model.load('scuola.xml')  """

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u'Denominazione scuola'),
        required=True,
    )

    cod_meccanografico = schema.TextLine(
        title=_(u'label_title', default=u'Codice istituto'),
        description=_(u'Codice ministeriale'),
        required=True,
    )
    email_istituzionale = Email(
        title=_(u'label_title', default=u'Email istituzionale'),
        description=_(u'Posta elettronica istituzionale @istruzione.it'),
        required=False,
    )
    tipo_istituto = schema.TextLine(
        title=_(u'label_title', default=u'Tipo istituto'),
        description=_(u'Tipologia di istituto (liceo scientifico, industriale, ecc...)'),
        required=False,
    )
    indirizzo = schema.TextLine(
        title=_(u'label_title', default=u'Indirizzo scuola'),        
        required=False,
    )
    cap = schema.TextLine(
        title=_(u'label_title', default=u'CAP'),
        required=False,
    )
    telefono = schema.TextLine(
        title=_(u'label_title', default=u'Telefono scuola'),
        required=False,
    )
    provincia = schema.TextLine(
        title=_(u'label_title', default=u'Provincia'),
        required=False,
    )
    ambito = schema.TextLine(
        title=_(u'label_title', default=u'Denominazione ambito'),
        required=False,
    )
    comune = schema.TextLine(
        title=_(u'label_title', default=u'Comune'),
        required=False,
    )
    dirigente = schema.TextLine(
        title=_(u'label_title', default=u'Dirigente Scolastico'),
        description=_(u'Nome e cognmome del dirigente'),
        required=False,
    )
    tipo_incarico = schema.TextLine(
        title=_(u'label_title', default=u'Incarico del dirigente'),
        description=_(u'indica se effettivo o in reggenza'),
        required=False,
    )
    ref_name = schema.TextLine(
        title=_(u'label_title', default=u'Referente - nominativo'),
        description=_(u'Nome e Cognome del docente referente della scuola'),
        required=False,
    )
    ref_email = Email(
        title=_(u'label_title', default=u'Referente - email'),
        description=_(u'Email del referente'),
        required=False,
    )
    pec = Email(
        title=_(u'label_title', default=u'PEC istituzionale'),
        required=False,
    )
    ref_mobile = schema.TextLine(
        title=_(u'label_title', default=u'Referente - telefono'),
        description=_(u'Riferimento telefonico del referente'),
        required=False,
    )
    




@implementer(IScuola)
class Scuola(Container):
    """
    """
    @property
    def id(self):
        if self.cod_meccanografico is None:
            return ''
        return self.cod_meccanografico.lower()
    
    @id.setter
    def id(self,value):
        pass
    
    """ DA CONTROLLARE """
    