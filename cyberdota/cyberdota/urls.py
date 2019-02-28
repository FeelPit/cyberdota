"""cyberdota URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from cyberdota import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'welcome/', views.welcome_page),
    url(r'reg/$', views.registration),
    url(r'main/$', views.main_page),
    url(r'login/$', views.login),
    url(r'search/$', views.search_choice),
    path(r'search/auto/', views.search_auto),
    url(r'create/$', views.create_team),
    path(r'profile/<int:idha>/', views.profile),
    url(r'main_menu/$', views.menu),
    path(r'add/<str:team>/<str:name>/<str:dec>', views.add),
    path(r'match/<str:match_id>', views.match),
    path(r'team/<int:team_id>', views.team),
    path(r'api/team_invite/<int:team_id>/<int:player_id>', views.api_teaminvite),
    url(r'exit/', views.exit),
    path(r'api/api_teamsrating', views.api_teamsrating),
    url(r'test/$', views.test)
]
