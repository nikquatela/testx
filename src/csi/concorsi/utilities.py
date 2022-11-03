# -*- coding: utf-8 -*-
from plone import api
from z3c.form.validator import SimpleFieldValidator
from zope.interface import Invalid


class PDFValidator(SimpleFieldValidator):

    def validate(self, value):
        super(PDFValidator, self).validate(value)
        request = api.portal.getRequest()
        req_object = request.get(self.widget.name)

        if req_object:
            if not getattr(req_object, 'filename', None):
                return

            if req_object.headers['content-type'] == 'application/pdf':
                return

            req_object.file.seek(0)
            try:
                if b'PDF' in next(req_object):
                    req_object.file.seek(0)
                    req_object.headers['content-type'] = 'application/pdf'
                    return
            except StopIteration:
                raise Invalid("il file che si sta tentando di caricare e' vuoto")

            api.portal.show_message(f"""controllare il campo: "{self.widget.label}" """,
                                    request=request,
                                    type="error")
            raise Invalid("Il file deve essere obbligatoriamente un PDF")
