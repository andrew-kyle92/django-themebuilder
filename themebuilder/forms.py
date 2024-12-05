import os

from django import forms
from django.apps import apps
from django.conf import settings

from .models.models import *


class Section:
    def __init__(self, legend, fields, sections=None):
        self.legend = legend
        self.fields = fields
        self.sections = sections


class ThemeForm(forms.Form):
    # theme portion
    theme_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'cols': '3'}), required=False)
    use_bootstrap = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-checkbox-input', 'checked': 'checked'}), help_text="Recommended", required=False)
    bootstrap_version = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "value": "5.3"}))
    is_active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-checkbox-input', "checked": "checked"}), required=False)

    # color scheme portion
    primary_color = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config', 'type': 'color', 'value': '#333333'}), required=False)
    secondary_color = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config', 'type': 'color', 'value': '#555555'}), required=False)
    background_color = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config', 'type': 'color', 'value': '#f0f0f0'}), required=False)
    text_color = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config', 'type': 'color', 'value': '#000000'}), required=False)
    accent_color = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config', 'type': 'color', 'value': '#ff5722'}), required=False)

    # typography portion
    font_family = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config'}), required=False)
    base_font_size = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config'}), required=False)
    h1_size = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config', 'style': 'width: 65px;'}), required=False)
    h2_size = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config', 'style': 'width: 65px;'}), required=False)
    h3_size = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config', 'style': 'width: 65px;'}), required=False)
    h4_size = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config', 'style': 'width: 65px;'}), required=False)
    h5_size = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config', 'style': 'width: 65px;'}), required=False)
    h6_size = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config', 'style': 'width: 65px;'}), required=False)

    # layout portion
    @staticmethod
    def get_template_choices(template_type):
        model = apps.get_model("themebuilder", template_type)
        templates_dir = os.path.join(settings.BASE_DIR, "themebuilder", "templates", "themebuilder", "layout", template_type + "s")
        custom_templates = model.objects.all()
        choices = [(template.pk, template.name) for template in custom_templates]
        for template in os.listdir(templates_dir):
            if os.path.isfile(os.path.join(templates_dir, template)):
                choices.append((template, template.strip('.html')))
        return choices

    header = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), required=False, choices=get_template_choices('header'))
    footer = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), required=False, choices=get_template_choices('footer'))
    container_width = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config'}), help_text="The width of the layout containers (e.g., '1200px' or '80%').", required=False)
    padding = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config'}), required=False)
    margin = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config'}), required=False)
    border_radius = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config'}), required=False)

    # animation portion
    animation_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config'}), help_text="The animation type to use. (e.g., 'fade', 'slide')", required=False)
    duration = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config'}), help_text="The duration (in seconds) of the animation.", required=False)
    delay = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control general-config'}), help_text="The delay (in seconds) of the animation.", required=False)

    custom_css = forms.CharField(widget=forms.Textarea(attrs={"hidden": True}), label="Custom CSS", help_text="The Custom CSS to use.", required=False)

    def __init__(self, *args, data=None, **kwargs):
        super().__init__(*args, **kwargs)

        if data is not None:
            for key, value in data.items():
                self.fields[key].initial = value

        self.sections = [
            Section(
                legend="Theme",
                fields=[self["theme_name"], self["description"], self["use_bootstrap"], self["bootstrap_version"], self["is_active"]],
            ),
            Section(
                legend="Style Attributes",
                fields=None,
                sections=[
                    Section(
                        legend="Color Scheme",
                        fields=[self["primary_color"], self["secondary_color"], self["background_color"], self["text_color"], self["accent_color"]]
                    ),
                    Section(
                        legend="Typography",
                        fields=[self["font_family"], self["base_font_size"]],
                        sections=[
                            Section(
                                legend="Heading Font Sizes",
                                fields=[self["h1_size"], self["h2_size"], self["h3_size"], self["h4_size"], self["h5_size"], self["h6_size"]],
                            )
                        ]
                    ),
                    Section(
                        legend="Animation",
                        fields=[self["animation_type"], self["duration"], self["delay"]]
                    ),
                    Section(
                        legend="Custom CSS",
                        fields=[self["custom_css"]]
                    )
                ]
            ),
            Section(
                legend="Layout",
                fields=[self["header"], self["footer"], self["container_width"], self["padding"], self["margin"], self["border_radius"]]
            )
        ]


class TemplateForm(forms.Form):
    name = forms.CharField(max_length=50)
    template = forms.FileField(max_length=50)
    # added fields not related to the model
    custom_path = forms.CharField(max_length=50, required=False)
    upload_path = forms.CharField(max_length=100, required=False)
    template_type = forms.CharField(max_length=50, required=False)


class TemplateBuilderForm(forms.Form):
    name = forms.CharField(label="Template Name", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    element = forms.ChoiceField(label="HTML Element", widget=forms.Select(attrs={'class': 'form-control'}))


class _TemplateBuilderForm(forms.Form):
    name = forms.CharField(label="Template Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    html = forms.CharField(widget=forms.Textarea(attrs={'class': 'codemirror', 'data-mode': 'htmlmixed'}))
    javascript = forms.CharField(widget=forms.Textarea(attrs={'class': 'codemirror', 'data-mode': 'javascript'}))
    css = forms.CharField(widget=forms.Textarea(attrs={'class': 'codemirror', 'data-mode': 'css'}))
