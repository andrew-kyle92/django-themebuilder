import json
import os.path

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView

from .forms import ThemeForm, TemplateForm, TemplateBuilderForm, _TemplateBuilderForm
from .models.models import Theme, Footer, Header
from .view_methods import *
from .utils.html_elements import HtmlElement


# Create your views here.
class IndexView(View):
    title = "Home | Theme Builder"
    template = "themebuilder/index.html"

    def get(self, request):
        context = {
            "title": self.title,
        }
        return render(request, self.template, context)


class CreateThemeView(View):
    title = "Create Theme | Theme Builder"
    template = "themebuilder/theme_form.html"
    form = ThemeForm()

    def get(self, request, *args, **kwargs):
        if kwargs.get('form', None):
            self.form = kwargs['form']
        pk = None
        context = {
            "title": self.title,
            "form": self.form,
            "theme_pk": pk,
        }
        return render(request, self.template, context)

    @staticmethod
    def post(request):
        form = ThemeForm(request.POST, request.FILES)
        if form.is_valid():
            theme = save_new_theme(form.cleaned_data, request.user)
            return redirect(reverse_lazy('view-theme', kwargs={'pk': theme.pk}))
        else:
            return redirect(reverse_lazy('create-theme', kwargs={'form': form}))


class ViewThemeView(View):
    title = "View Theme"
    template = "themebuilder/view_theme.html"

    def get(self, request, pk, *args, **kwargs):
        theme = Theme.objects.get(pk=pk)
        context = {
            "title": self.title,
            "theme": theme,
        }
        return render(request, self.template, context)


class UpdateThemeView(View):
    title = "Update Theme | Theme Builder"
    template = "themebuilder/theme_form.html"

    def get(self, request, pk):
        theme = Theme.objects.get(pk=pk)
        theme_data = get_theme_data(theme)
        form = ThemeForm(data=theme_data)
        context = {
            "title": self.title,
            "form": form,
            "theme_pk": theme.pk,
        }
        return render(request, self.template, context)

    def post(self, request, pk, *args, **kwargs):
        form = ThemeForm(request.POST, request.FILES)
        instance = Theme.objects.get(pk=pk)
        if form.is_valid():
            theme = save_existing_theme(form.cleaned_data, instance)
            return redirect(reverse_lazy('view-theme', kwargs={'pk': theme.pk}))
        else:
            return redirect(reverse_lazy('create-theme', kwargs={'form': form}))


class ThemePreviewView(View):
    title = "Theme Preview"
    template = "themebuilder/layout/layout_template.html"

    def get(self, request):
        try:
            default_theme = Theme.objects.get(pk=1)
        except Theme.DoesNotExist:
            default_theme = None
        r_theme = request.GET.get('pk')
        theme = Theme.objects.get(pk=int(r_theme)) if r_theme else default_theme
        header = get_template(theme, "header")
        footer = get_template(theme, "footer")
        default_header = "themebuilder/layout/headers/default_header.html"
        default_footer = "themebuilder/layout/footers/default_footer.html"
        context = {
            "title": self.title,
            "theme": theme,
            "header_type": header if header else default_header,
            "footer_type": footer if footer else default_footer,
        }
        return render(request, self.template, context)


class PreviewHeaderView(View):
    title = "Preview Header"
    template = "themebuilder/layout/snippet_template.html"

    def get(self, request):
        try:
            default_theme = Theme.objects.get(pk=1)
        except Theme.DoesNotExist:
            default_theme = None
        r_theme = request.GET.get('pk')
        theme = Theme.objects.get(pk=int(r_theme)) if r_theme else default_theme
        header_path = os.path.join(settings.BASE_DIR, 'themebuilder', 'templates')
        requested_header = request.GET.get("requestedHeader", None)
        if requested_header:
            if requested_header.isdigit():
                header = Header.objects.get(pk=int(requested_header))
                snippet = os.path.join("themebuilder", "layout", "headers", header.template.path)
            else:
                snippet = os.path.join(header_path, "themebuilder", "layout", "headers", requested_header)
        else:
            default_header = os.path.join("themebuilder", "layout", "headers", "default_header.html")
            if theme:
                if theme.layouts.first().header.isdigit():
                    header = Header.objects.get(pk=int(theme.layouts.first().header))
                    snippet = header.template.path
                else:
                    snippet = os.path.join(header_path, theme.layouts.first().header)
            else:
                snippet = os.path.join(header_path, default_header)

        context = {
            "title": self.title,
            "theme": theme,
            "snippet": snippet
        }
        return render(request, self.template, context)


class PreviewFooterView(View):
    title = "Preview Footer"
    template = "themebuilder/layout/snippet_template.html"

    def get(self, request):
        try:
            default_theme = Theme.objects.get(pk=1)
        except Theme.DoesNotExist:
            default_theme = None
        r_theme = request.GET.get('pk')
        theme = Theme.objects.get(pk=int(r_theme)) if r_theme else default_theme
        footer_path = os.path.join(settings.BASE_DIR, "themebuilder", "templates", "layout", "footers", "custom")
        requested_footer = request.GET.get("requestedFooter", None)
        if requested_footer:
            if requested_footer.isdigit():
                footer = Footer.objects.get(pk=int(requested_footer))
                snippet = footer.template.path
            else:
                snippet = os.path.join(footer_path, requested_footer)
        else:
            default_footer = "themebuilder/layout/footers/default_footer.html"
            snippet = get_template(theme, "footer") if theme else default_footer
        context = {
            "title": self.title,
            "theme": theme,
            "snippet": snippet,
        }
        return render(request, self.template, context)


class ThemesListView(ListView):
    title = "Themes"
    template_name = "themebuilder/themes_list.html"
    model = Theme

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class TemplateBuilderView(View):
    title = "Template Builder"
    template_name = "themebuilder/_template_builder.html"
    form = _TemplateBuilderForm

    def get(self, request):
        context = {
            "title": self.title,
            "form": self.form,
        }
        return render(request, self.template_name, context)


# ##### Fetch Requests #####
def upload_template(request):
    form = TemplateForm(request.POST, request.FILES)

    if request.method == "POST":
        if form.is_valid():
            template_type = form.cleaned_data["template_type"]
            model = apps.get_model("themebuilder", template_type)
            try:
                instance = model(
                    name=form.cleaned_data["name"],
                    template=form.cleaned_data["template"],
                    path=form["upload_path"] if form["custom_path"] else None,
                )
                instance.save()
                template_choices = get_template_choices(template_type)
                return JsonResponse({"status": "success", "choices": template_choices}, safe=True)
            except Exception as e:
                return JsonResponse({"status": "fail", "msg": e}, safe=True)
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, safe=True)
    else:
        return JsonResponse({"status": "error", "msg": "This method only accepts POST requests"}, safe=True)


def retrieve_element_attributes(request):
    element = request.GET.get("element", None)
    if element is not None:
        html_element = HtmlElement()
        element = html_element.get_element(element)
        return JsonResponse({"status": "success", "element": element}, safe=True)
    else:
        return JsonResponse({"status": "error", "msg": "Element is not provided"}, safe=True)
