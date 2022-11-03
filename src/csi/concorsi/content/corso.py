# -*- coding: utf-8 -*-
from csi.concorsi import _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from plone.autoform import directives


import re

regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

class ICorso(model.Schema):
    """ Marker interface for Corso
    """

    """ model.load('corso.xml')  """

    title = schema.TextLine(
        title=_(u'Tematica generale'),
        required=False,
    )

    description = schema.Text(
        title=_(u'Descrizione'),
        description=_(u"Usato nell'elenco degli elementi e nei risultati delle ricerche"),
        required=False,
    )

    dipartimento = schema.TextLine(
        title=_(u'label_title', default=u'Dipartimento'),
        description=_(u'dipartimento erogante il corso'),
        required=False,
    )

    sede = schema.TextLine(
        title=_(u'label_title', default=u'Sede del dipartimento erogante il corso'),
        description=_(u'Sede del corso'),
        required=False,
    )

    seminari = schema.TextLine(
        title=_(u'label_title', default=u'Seminari/Laboratori'),
        required=False,
    )

    n_posti = schema.Int(
        title=_(u'label_title', default=u'N. max studenti'),
        required=False,
    )

    info_calendario = schema.Text(
        title=_(u'label_title', default=u'Calendario'),
        required=False,
    )

    esonero = schema.Bool(
        title=_(u'label_title', default=u'Esonero prove ingresso CLNP'),
        description=_(u"Esonero dalle prove di ingresso per i CL a numero programmato"),
        required=False,
    )

    cfu_utili = schema.Bool(
        title=_(u'label_title', default=u'CFU utilizzabili'),
        description=_(u"CFU utilizzabili fra le attivita a scelta libera"),
        required=False,
    )

    n_cfu = schema.Int(
        title=_(u'label_title', default=u'CFU attribuibili'),
        required=False,
    )

    punteggio_clnp = schema.Bool(
        title=_(u'label_title', default=u'Attribuzione di punteggio nei CLNP'),
        description=_(u"Eventuale attribuzione di punteggio nel clnp a livello locale"),
        required=False,
    )

    referente = schema.Text(
        title=_(u'label_title', default=u'Referenti'),
        description=_(u"Uno o piu' referenti. E' necessario specificare per ognuno la mail @uniba.it"),
        required=False,
    )

    docente_delegato = schema.Text(
        title=_(u'label_title', default=u'Docente delegato'),
        description=_(u"Docente Delegato all'orientamento"),
        required=False,
    )
    directives.omitted('docente_delegato')

    info_link = schema.Text(
        title=_(u'label_title', default=u'Didattica a distanza - info/link'),
        description=_(u"Informazioni sulla didattica a distanza. Eventuale link diretto per collegamento"),
        required=False,
    )

    note = schema.Text(
        title=_(u'label_title', default=u'Note'),
        description=_(u"Note informative"),
        required=False,
    )






@implementer(ICorso)
class Corso(Container):
    """
    """

    """ DA CONTROLLARE """

    def getUsernameFromReferente(self,):
        """ parserizza il campo referente per estrarre la username
        """
        referente = self.getReferente()
        for first in self._get_emails(referente):
            yield first[:first.find('@')]

    def _get_emails(self, s):
        """Returns an iterator of matched emails found in string s."""
        # Removing lines that start with '//' because the regular expression
        # mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
        return (email[0] for email in re.findall(regex, s) if not email[0].startswith('//'))

    def getIscrizioneUrl(self,):
        """ restituisce un url da cui popolare l'adesione al corso
        """
        from plone import api

        if api.user.is_anonymous():
            return None

        portal = api.portal.getSite()
        scuoleFolder = portal.get('scuole', None)
        if not scuoleFolder:
            return None

        user = api.user.get_current()
        try:
            homeid = user.getId()
        except:
            return None

        home = scuoleFolder.get(homeid)
        uid = self.UID()

        return home.absolute_url() + '/iscrizione?corsouid=' + uid

    def getNScuoleAderenti(self,):
        """
        """
        adesioni = self.getBackReferences('adesione_corso')
        adesioni_ositive = [
            a for a in adesioni if a is not None and len(a.studenti) > 0]

        return len(adesioni_ositive)

    def getInfo_link(self,):
        """ riformatta il testo per includere degi anchor
        """
        value = self.getRawInfo_link()
        tokens = value.split()
        for i,token in enumerate(tokens):
            islink = False
            if token.startswith('http'):
                islink = True
            if token.startswith('www'):
                islink = True
                token = "https://"+ token
            if islink:
                tokens[i] = '''<a href="{}">{}</a>'''.format(token,  token[:50]+'[...]', )

        output = ' '.join(tokens)
        return output