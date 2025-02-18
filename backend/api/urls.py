from django.urls import path, include

from api.views import CategoryListView


urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('category/', CategoryListView.as_view(), name='category')
]
