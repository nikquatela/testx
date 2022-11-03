# -*- coding: utf-8 -*-
from csi.concorsi import _
from plone.app.dexterity.behaviors.metadata import _ as _p
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import implementer


class IConcorsoAssRicerca(model.Schema):
    """ Marker interface for ConcorsoAssRicerca
    """

    model.load('concorso_ass_ricerca.xml') 

    struttura = schema.Tuple(
        title=_(u'Struttura di assegnazione'),
        value_type=schema.TextLine(),
        required=False,
        missing_value=[],
    )
    directives.omitted('struttura')

    codice_concorso = schema.TextLine(
        title=_p(u'label_title', default=u'Codice Concorso'),
        description=_(u'numero bando / anno di pubblicazione'),
        required=False,
    )
    directives.omitted('codice_concorso')
    
    fieldset('dati_bando',
        label=_(u'dati_bando', default=u'Dati bando'),
        fields=[
            "dr_bando",
            "data_bando",
            "scadenza_termini",
            "_allegatobando",
        ]
    )

    fieldset("dati_bando_riapertura",
        label=_(u'dati_bando_riapertura', default=u'Dati bando - riapertura'),
        fields=[
            "dr_modif_riap",
            "data_bando_MR",
            "_allegato_DR_modif",
            "data_GU_MR",
            "scadenza_termini_MR",
        ]
    )


    fieldset('commissione',
        label=_(u'commissione', default=u'Commissione'),
        fields=[
            '_allegato_DR_commissione',
            'allegato_valutazionetitoli',
            'allegato_valutazionecolloquio',
        ]
    )


    fieldset("approvazione_atti",
        label=_(u'approvazione_atti', default=u'Approvazione atti'),
        fields=[
            "_allegato_DR_atti",
        ]
    )

    fieldset("note",
        label=_(u'note', default=u'Note'),
        fields=[
            "note",
        ]
    )






@implementer(IConcorsoAssRicerca)
class ConcorsoAssRicerca(Container):
    """
    """
    
    @property
    def title(self):
        if hasattr(self, 'dr_bando') and hasattr(self,'data_bando'):
            data_bando = self.data_bando and self.data_bando.strftime("%d/%m/%Y") or '--incompleto'
            titolo = 'A.R. Prog. {} Sett. {} D.R. n. {} del {}'.format(
                self.programma_ricerca,
                self.settoreDisciplinare,
                self.dr_bando,
                data_bando,
            )
        else:
            titolo = ''
        return titolo
    
    @title.setter
    def title(self,value):
        pass


    def approvato(self):
        '''restituisce vero se esiste un decreto di approvazione atti'''
        attr = getattr(self, '_allegato_DR_atti', None)
        if attr:
            return True
        else:
            return False

    def scadenza(self):
        if self.scadenza_termini_MR:
            return self.scadenza_termini_MR
        else:
            return self.scadenza_termini
