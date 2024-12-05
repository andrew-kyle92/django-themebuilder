from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('editor/', TemplateView.as_view(template_name="editor.html"), name='editor'),
    path('create-theme/', views.CreateThemeView.as_view(), name='create-theme'),
    path('view-theme/<pk>/', views.ViewThemeView.as_view(), name='view-theme'),
    path('update-theme/<pk>/', views.UpdateThemeView.as_view(), name='update-theme'),
    path('theme-preview/', views.ThemePreviewView.as_view(), name='theme-preview'),
    path('preview-header/', views.PreviewHeaderView.as_view(), name='preview-header'),
    path('preview-footer/', views.PreviewFooterView.as_view(), name='preview-footer'),
    path('themes/', views.ThemesListView.as_view(), name='themes'),
    path('template-builder/', views.TemplateBuilderView.as_view(), name='template-builder'),
    # ##### Fetch Requests #####
    path('upload-template/', views.upload_template, name='upload-template'),
    path('get-element/', views.retrieve_element_attributes, name='get-element'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
