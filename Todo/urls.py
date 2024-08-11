from django.urls import path
from . import views
urlpatterns = [
    path('',views.Home,name='home'),
    path('add/',views.add,name="add"),
    path('detete/<int:pk>/',views.delete,name="delete"),
    path('todolist/',views.todolist,name="todolist")
]