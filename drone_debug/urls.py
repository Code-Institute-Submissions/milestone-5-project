"""drone_debug URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.views.generic.base import RedirectView
from .settings import MEDIA_ROOT

favicon_view = RedirectView.as_view(url='favicon/favicon.ico', permanent=True)

urlpatterns = [
    path('favicon.ico/', favicon_view, name="favicon"),
    path('', include('landing_page.urls')),
    path('posts/', include('blog.urls')),
    path('issues/', include('issue_tracker.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('userprofile.urls')),
    path('search/', include('search.urls')),
    re_path('media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
