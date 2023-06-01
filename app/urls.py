from django.urls import path
from . import views
urlpatterns = [
    path('',views.api_overview,name='api_overview'),
    path('create/',views.create_data,name="create_data"),
    path('all/',views.get_all_count,name="get_all_count"),
    path('update/<int:pk>',views.Update_Student_count,name="Update_Count"),
    path('pdf_gen',views.pdf_gen,name="pdf_gen"),
    path('loop',views.create_Loop,name="create_loop")
]