from django.urls import path,include
from home.views import index,people,login,personAPI,PeopleViewSet,registerapi,LoginAPI

from rest_framework.routers import DefaultRouter
router =DefaultRouter()
router.register(r'people',PeopleViewSet,basename='people')
urlpatterns=router.urls

urlpatterns = [

    path('login/', LoginAPI.as_view()),
    path('index/', index),
    path('person/', people),
    path('login/', login),
    path('persons/',personAPI.as_view()),
    path('',include(router.urls)),
    path('register/',registerapi.as_view()),    
    
]
