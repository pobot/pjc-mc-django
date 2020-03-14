"""pjc_mc_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import RedirectView

admin.site.site_header = "POBOT Junior Cup"
admin.site.index_title = "POBOT Junior Cup - Administration"

urlpatterns = [
    url(r'^favicon.ico$', RedirectView.as_view(url=static('/img/favicon.png'))),
    url(r'^admin/', admin.site.urls),
    url(r'^display/', include('display.urls')),
    url(r'^refereeing/', include('refereeing.urls', namespace='refereeing')),
    url(r'^finals/', include('event.urls', namespace='finals')),
]
