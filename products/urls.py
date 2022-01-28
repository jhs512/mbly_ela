from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('<int:product_id>/', views.product_detail, name='detail'),
    path('<int:product_id>/question/create/', views.question_create, name='question_create'),
    path('<int:product_id>/question/delete/<int:question_id>', views.question_delete, name='question_delete'),
    path('<int:product_id>/question/modify/<int:question_id>', views.question_modify, name='question_modify'),
    path('<int:product_id>/pick/', views.product_pick, name='pick'),
    path('<int:product_id>/picked/', views.product_unpick, name='unpick'),
    path('admin_api/', views.AdminApiProductListCreateView.as_view(), name='admin_api'),
    path('admin_api/<int:pk>/', views.AdminApiProductRetrieveUpdateDestroyView.as_view(), name='admin_api_item'),
    path('admin_api/<int:product_id>/reals/', views.AdminApiProductRealListCreateView.as_view(), name='admin_api_reals'),
]
