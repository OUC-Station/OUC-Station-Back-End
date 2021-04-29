"""station URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),

    path('api/location/', include(('apps.location.urls', 'apps.location'), namespace='location')),
    path('api/activity/', include(('apps.activity.urls', 'apps.activity'), namespace='activity')),
    path('api/account/', include(('apps.account.urls', 'apps.account'), namespace='account')),
    path('api/bbs/', include(('apps.bbs.urls', 'apps.bbs'), namespace='bbs')),
    path('api/suggestion/', include(('apps.suggestion.urls', 'apps.suggestion'), namespace='suggestion')),
]
