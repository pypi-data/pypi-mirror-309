from django.urls import path
from .views import DynamicListView

urlpatterns = [
    path('<str:app_label>/<str:model_name>/', DynamicListView.as_view(), name='dynamic-list-view'),
]

