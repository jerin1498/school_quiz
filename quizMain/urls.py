"""quizMain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from .views import home
from mcQuiz.views import QuizList

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', QuizList.as_view(), name='quiz-list'),
    url(r'^$', home, name='home'),
    url(r'^quiz/', include('mcQuiz.urls', namespace='quiz')),
    url(r'^account/', include('accounts.urls', namespace='account')),

]


if settings.DEBUG:
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
