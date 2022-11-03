# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from csi.concorsi import _
from email.policy import default
from plone.app import textfield
from plone.app.dexterity.behaviors.metadata import _ as _p
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.interfaces import IAddForm
from zope import schema
from zope.interface import implementer, Invalid, invariant


class IConcorsoRicercatore(model.Schema):
    """ Marker interface for Concorso
    """

    model.load('concorso.xml')

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_p(u'label_title', default=u'Title'),
        required=False,
    )
    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_p(u'label_description', default=u'Summary'),
        description=_p(
            u'help_description',
            default=u'Used in item listings and search results.'
        ),
        required=False,
        missing_value=u'',
    )

    directives.order_before(description='*')
    directives.order_before(title='*')

    directives.no_omit(IAddForm, 'description')
    directives.omitted('title')  

    codice_concorso = schema.TextLine(
        title=_p(u'label_title', default=u'Codice Concorso'),
        description=_(u'numero bando / anno di pubblicazione'),
        required=False,
    )
    directives.omitted('codice_concorso')

    rapporto = schema.Choice(
         title=_(u'Rapporto di lavoro'),
         description=_(u'Descrive il tipo di contratto'),
         vocabulary='csi.concorsi.rapportoConcorsoRicercatore',
         required=True,
    )
    directives.widget(
        'rapporto',
        RadioFieldWidget,
    )
    directives.order_after(rapporto='description')

    struttura = schema.Tuple(
        title=_(u'Struttura di assegnazione'),
        description=_(u'La struttura dove verra'' impiegato il vincitore'),
        value_type=schema.TextLine(),
        required=False,
        missing_value=[],
        max_length=1,
    )
    directives.widget(
        'struttura',
        AjaxSelectFieldWidget,
        vocabulary='csi.concorsi.vocabularies.ListaStrutture',
    )
    directives.order_before(struttura='nr_posti')

    settoreConcorsuale = schema.TextLine(
        title=_(u'Settore Concorsuale'),
        required=False,
    )
    
    settoreDisciplinare = schema.TextLine(
        title=_(u'Settore scientifico disciplinare'),
        required=False,
    )

    criteriValutazione = field.NamedBlobFile(
        title=_(u'Criteri di valutazione'),
        description=_(u'allegare i criteri di valutazione'),
        required=False,
    )

    fieldset('dati_bando',
        label=_(u'dati_bando', default=u'Dati bando'),
        fields=[
            "dr_bando",
            "data_bando",
            "pubbl_GU",
            "data_GU",
            "scadenza_termini",
            "AlboPretorioOnline",
            "data_AlboPretorioOnline",
            "_allegatobando",
            "_allegato_A",
        ]
    )

    fieldset("dati_bando_riapertura",
        label=_(u'dati_bando_riapertura', default=u'Dati bando - riapertura'),
        fields=[
            "dr_modif_riap",
            "data_bando_MR",
            "_allegato_DR_modif",
            "pubb_GU_MR",
            "data_GU_MR",
            "scadenza_termini_MR",
        ]
    )


    nota_prove = textfield.RichText(
        title=_(u'Espletamento procedura'),
        required=False,
    )
    fieldset('prove',
        label=_(u'prove', default=u'Prove'),
        fields=[
            'nota_prove',
            'nr_domande',
        ]
    )
    directives.omitted('per_titoli')
    directives.omitted('prove')
    directives.omitted('date_espletamento')

    fieldset('commissione',
        label=_(u'commissione', default=u'Commissione'),
        fields=[
            'Comm_nominata',
            'DR_commissione',
            'data_DR_commissione',
            '_allegato_DR_commissione',
            'componenti_commissione',
            'AlboPretorioOnlineCommissione',
            'data_AlboPretorioOnlineCommissione',
            "criteriValutazione",
        ]
    )

    """ dataDiscussionePubblica = schema.Datetime(
        title=_(u'Data discussione pubblica'),
        required=False,
    ) """
    """ fieldset("date_concorso", 
        label=_(u'date_concorso', default=u'Date concorso'),
        fields=[
            "dataDiscussionePubblica",
        ]
    ) """
    """ directives.omitted('dataDiscussionePubblica') """


    fieldset("approvazione_atti",
        label=_(u'approvazione_atti', default=u'Approvazione atti'),
        fields=[
            "DR_appr_atti",
            "data_DR_appr_atti",
            "_allegato_DR_atti",
            "modifiche_atti",
            "vincitore",
            "assunzione",
            "spesa_concorsuale",
            "candidatiassunti",
            "AlboPretorioOnlineAtti",
            "data_AlboPretorioOnlineAtti",
        ]
    )

    fieldset("note",
        label=_(u'note', default=u'Note'),
        fields=[
            "note",
        ]
    )

    prove = schema.Tuple(
        title=_(u'Prove'),
        description=_(u'Elenco delle prove del concorso'),
        value_type=schema.TextLine(),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'prove',
        AjaxSelectFieldWidget,
        vocabulary='csi.concorsi.vocabularies.ListaProve',
    )

    @invariant
    def CheckApprovazioneAtti(data):
        dr = data.DR_appr_atti
        daradr = data.data_DR_appr_atti
        alldr = data._allegato_DR_atti
        # nel caso di approvazione atti i tre campi devono essere tutti compilati
        if dr is not None or daradr is not None or alldr is not None:
            if dr is None or daradr is None or alldr is None:
                raise Invalid("Attenzione, controllare i dati del decreto di approvazione atti")

    @invariant
    def CheckCommissione(data):
        isNominata = data.Comm_nominata
        commdr = data.DR_commissione
        daradr = data.data_DR_commissione
        allgdr = data._allegato_DR_commissione
        # nel caso di commissione nominata i tre campi devono essere tutti compilati
        if isNominata:
            if commdr is None or daradr is None or allgdr is None:
                raise Invalid("Attenzione, controllare i dati del decreto di nomina della commissione")

    @invariant
    def CheckGazzettaUfficiale(data):
        pubbl_GU = data.pubbl_GU
        data_GU = data.data_GU
        # nel caso il numero della gazzetta ufficile sia differente da 0 (default) deve essere compilata la data
        if pubbl_GU is not None:
            if pubbl_GU > 0 and data_GU is None:
                raise Invalid("Attenzione, inserire la data di pubblicazione della gazzetta ufficiale")

@implementer(IConcorsoRicercatore)
class ConcorsoRicercatore(Container):
    """
    """
    
    @property
    def title(self):
        if hasattr(self, 'dr_bando') and hasattr(self,'data_bando'):
            dr_bando = self.dr_bando or ""
            data_bando = self.data_bando or ""
            return dr_bando + '/' + str(data_bando)[2:4]
        else:
            return ''
    
    @title.setter
    def title(self,value):
        pass

    def approvato(self):
        '''restituisce vero se esiste un decreto di approvazione atti'''
        attr = getattr(self, 'DR_appr_atti', None)
        if attr:
            return True
        else:
            return False

    def scadenza(self):
        if self.scadenza_termini_MR:
            return self.scadenza_termini_MR
        else:
            return self.scadenza_termini
