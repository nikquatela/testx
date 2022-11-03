# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api
from plone.dexterity.browser.view import DefaultView
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

       
class IConcorsoView(Interface):
    """ Marker Interface for IConcorsoView"""

class ConcorsoView(DefaultView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('concorsoview.pt')

    def htmlintelligent(self, campo_list):
        campo_string = '\n'.join(campo_list)
        # Transform plain text description with ASCII newlines to one with
        portal_transforms = api.portal.get_tool(name='portal_transforms')
        # Output here is a single <p> which contains <br /> for newline
        data = portal_transforms.convertTo('text/html', campo_string, mimetype='text/x-web-intelligent')
        html = data.getData()
        return html
        
    def __call__(self):
        # Implement your own actions:
        self._update()
        self.update()
        return self.index()

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def isExpired(self, data_ultimo_termine):
        now = datetime.now()
        if data_ultimo_termine < now:
            return True
        else:
            return False

    def getURL(self, nome_campo):
        download_url=''
        file_to_download = self.context.__getattribute__(nome_campo)
        if(file_to_download is not None):
            file_to_download_name = file_to_download.filename
            download_url='view/++widget++form.widgets.'+nome_campo+'/@@download/'+file_to_download_name
        return download_url

    def batch(self):
        """ ritorna la lista di tutti gli oggetti di tipo Nota presenti nel Concorso ordinati per ultima modifica"""
        context = self.context
        filtri = {'portal_type': 'Nota',
            'sort_on': 'CreationDate',
            'sort_order': 'descending'}
        brains = context.getFolderContents(contentFilter=filtri)
        return brains

    def getTitle(self):
        context = self.context

        if context.dr_bando and context.data_bando and context.nr_posti:
            """ titolo = 'Concorso Pubblico per la copertura di n. '+str(context.nr_posti)
            titolo = titolo + (' posti ' if context.nr_posti>1 else ' posto ')
            if len(context.categoria)>0:
                titolo = titolo + 'di cat. '+str(context.categoria[0])
            if len(context.struttura)>0:
                titolo = titolo + ' per la struttura '+str(context.struttura[0])
            titolo = titolo + ' - Bando '+context.dr_bando + '/' + str(context.data_bando)[2:4] """
            titolo = 'Concorso '+context.dr_bando + '/' + str(context.data_bando)[2:4]
            return titolo
        else:
            return ''



class concorsoRicercatoreView(ConcorsoView):
    """ vista default concorso a ricercatore
    """
    def getTitle(self):
        context = self.context
        if context.dr_bando and context.data_bando and context.nr_posti:
            """ titolo = 'Selezione pubblica per la copertura di n. '+str(context.nr_posti)
            posti = ' posti ' if context.nr_posti>1 else ' posto '
            rapporto = ' di ricercatore universitario ' if context.rapporto=='Ricercatore' else ' di professore associato '
            titolo = titolo + posti + rapporto + ' - Bando '+context.dr_bando + '/' + str(context.data_bando)[2:4] """
            
            titolo = 'Selezione '+context.dr_bando + '/' + str(context.data_bando)[2:4]
            return titolo
        else:
            return ''

    
    def getCreationDate(self, nome_campo):
        file_to_download = self.context.__getattribute__(nome_campo)
        if(file_to_download is not None):
            file_to_download_date = datetime.fromtimestamp(file_to_download._p_mtime)
        return file_to_download_date



class concorsoAssRicercaView(ConcorsoView):
    """ vista default concorso assegno di ricerca
    """
