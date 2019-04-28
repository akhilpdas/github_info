from rest_framework import routers
from rest_framework.routers import SimpleRouter
from django.urls import path
from user_info.views import *

urlpatterns = [
    path('search',SearchView.as_view(),name='SearchView'),
    path('result',ResultView.as_view(),name='ResultView'),
    path('credentials',CredentialsView.as_view(),name='CredentialsView'),

]
router = SimpleRouter(trailing_slash=False)

urlpatterns += router.urls

