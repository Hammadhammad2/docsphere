from django.urls import path

from organizations import views

urlpatterns = [
    path('', views.OrganizationListView.as_view(), name='list'),
    path('<int:id>/', views.OrganizationDetailView.as_view(), name='detail'),
    path('create/', views.OrganizationCreateView.as_view(), name='create'),
    path('update/<int:id>/', views.OrganizationUpdateView.as_view(), name='update'),
]
