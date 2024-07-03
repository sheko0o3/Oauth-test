from django.urls import path, include
from django.contrib import admin


admin.autodiscover()


from . import views


# Setup the URLs and include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', views.UserList.as_view()),
    path('users/<pk>/', views.UserDetails.as_view()),
    path('groups/', views.GroupList.as_view()),
    path("creatuser/", views.CreateUser.as_view()),
    path("gettoken/", view=views.Token.as_view()),
    path("", include("rest_framework.urls"))
    # ...
]


