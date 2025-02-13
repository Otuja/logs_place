from django.urls import path
from .views import add_social_account, social_accounts_list, update_social_account, delete_social_account, filter_social_accounts, social_account_detail, index

app_name = 'products'

urlpatterns = [
    path('', index, name='index'),
    path('add/', add_social_account, name='add_social_account'),
    path('list/', social_accounts_list, name='social_accounts_list'),
    path('filter-accounts/', filter_social_accounts, name='filter_accounts'),
    path('social-account/<uuid:pk>/', social_account_detail, name='social_account_detail'),  # UUID as PK
    path('update/<uuid:pk>/', update_social_account, name='update_social_account'),
    path('delete/<uuid:pk>/', delete_social_account, name='delete_social_account'),
]
