
from django.apps import apps
from django.template.response import TemplateResponse
from django.urls import NoReverseMatch, reverse
from django.utils.text import capfirst
from django.utils.translation import gettext as _, gettext_lazy
from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib import admin
from django.http import FileResponse
import re

from service_report.services import PDFService


class MyAdminSite(AdminSite):

    def _build_app_dict(self, request, label=None):
        """
        Build the app dictionary. The optional `label` parameter filters models
        of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_admin in models.items():
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True not in perms.values():
                continue

            info = (app_label, model._meta.model_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'perms': perms,
                'admin_url': None,
                'add_url': None,
                'index': getattr(model_admin, 'index', 500),
            }
            if perms.get('change') or perms.get('view'):
                model_dict['view_only'] = not perms.get('change')
                try:
                    model_dict['admin_url'] = reverse(
                        'admin:%s_%s_changelist' % info, current_app=self.name)
                except NoReverseMatch:
                    pass
            if perms.get('add'):
                try:
                    model_dict['add_url'] = reverse(
                        'admin:%s_%s_add' % info, current_app=self.name)
                except NoReverseMatch:
                    pass

            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_index = getattr(
                    apps.get_app_config(app_label), "index", 500)
                app_dict[app_label] = {
                    'name': '[%s] %s' % (app_index, apps.get_app_config(app_label).verbose_name),
                    'app_label': app_label,
                    'app_url': reverse(
                        'admin:app_list',
                        kwargs={'app_label': app_label},
                        current_app=self.name,
                    ),
                    'has_module_perms': has_module_perms,
                    'models': [model_dict],
                    'index': getattr(apps.get_app_config(app_label), "index", 500),
                }

        if label:
            return app_dict.get(label)
        return app_dict

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['index'])

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['index'])

        return app_list

    def app_index(self, request, app_label, extra_context=None):
        app_dict = self._build_app_dict(request, app_label)
        if not app_dict:
            raise Http404('The requested admin page does not exist.')
        # Sort the models alphabetically within each app.
        app_dict['models'].sort(key=lambda x: x['index'])
        app_name = apps.get_app_config(app_label).verbose_name
        context = {
            **self.each_context(request),
            'title': _('%(app)s administration') % {'app': app_name},
            'app_list': [app_dict],
            'app_label': app_label,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.app_index_template or [
            'admin/%s/app_index.html' % app_label,
            'admin/app_index.html'
        ], context)


custom_admin = MyAdminSite(name="custom_admin")


class NotDefinedReport(PDFService):
    title = "report_not_defined"


class ModelAdminWithPDF(ModelAdmin):
    change_form_template = "admin/change_form_with_pdf_iframe.html"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name
        my_urls = [
            path('report/<path:object_id>', self.report_view,
                 name='%s_%s_report' % info),
        ]
        return urls + my_urls

    def report_view(self, request, object_id):
        pdf = NotDefinedReport()
        buffer = pdf.get_buffer()
        return FileResponse(buffer, as_attachment=False, filename='hello.pdf')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra = extra_context or {}
        pdf_url = re.compile(
            r'/(\d+)/change/').sub(r'/report/\1', request.path_info)
        # print(pdf_url)
        extra['pdf_url'] = pdf_url
        return super().change_view(request, object_id,
                                   form_url, extra_context=extra)


def multi_line(value_dict={}):
    keys = f'<div style="display:inline-block;text-align:right; margin-right:5px;">{"<br>".join(value_dict.keys())}</div>'
    values = f'<div style="display:inline-block">{"<br>".join(value_dict.values())}</div>'
    return keys + values
