"""
URL configuration for Pet_Adoption_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from Home.views import *;
from Login.views import *;

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Pet_Home,name="Pet_Home"),
    path('adoption/',Pet_Adoption_Form,name="Pet_Adoption_Form"),
    path('detail/<id>/',Pet_Detail,name="Pet_Detail"),
    path('list/',Pet_List,name="Pet_List"),
    path('contact/',Pet_Contact,name="Pet_Contact"),

    path('myfavs/',My_Favourites,name="My_Favourites"),
    path('favourite/<id>/',Add_Favourite,name="Add_Favourite"),
    path('deletefav/<id>/',Delete_Favourite,name="Delete_Favourite"),

    path('mynotifys/',My_Notifications,name="My_Notifications"),
    path('notification/<id>/',Notification,name="Notification"),
    path('acceptnotifys/<id>/',Accept_Notification,name="Accept_Notification"),
    path('deletenotifys/<id>/',Delete_Notify,name="Delete_Notify"),

    path('adopt_pet',Pet_Adopt,name="Pet_Adopt"),
    path('meet/',Pet_Meet,name="Pet_Meet"),

    path('login/',Pet_Login,name="Pet_Login"),
    path('signup/',Pet_Signup,name="Pet_Signup"),
    path('logout/',logout_page,name="logout_page")

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

