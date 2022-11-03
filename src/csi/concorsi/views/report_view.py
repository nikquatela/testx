# -*- coding: utf-8 -*-

from plone.app.contenttypes.browser.collection import CollectionView
from plone.dexterity.browser.view import DefaultView
from Products.CMFCore.interfaces import IFolderish
from Products.CMFPlone.PloneBatch import Batch
from zope.interface import Interface


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IReportView(Interface):
    """ Marker Interface for IConcorsoView"""

class ReportView(CollectionView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('bollettino_tab_view.pt')

    def batch(self):
        return self.results()

    def getURL(self, nome_campo, itemObj):
        download_url=''
        file_to_download = getattr(itemObj, nome_campo)
        id = itemObj.getId()
        if(file_to_download is not None):
            file_to_download_name = file_to_download.filename
            download_url=id+'/view/++widget++form.widgets.'+nome_campo+'/@@download/'+file_to_download_name
        return download_url

    def render(self):
        return self.index()

    def __call__(self):
        return self.index()
