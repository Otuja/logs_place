from django.urls import path
from .views import wallet_view, fund_wallet, monnify_webhook, order_list, purchase_account, submit_nin

urlpatterns = [
    path('wallet/', wallet_view, name='wallet_view'),
    path('wallet/nin/', submit_nin, name='submit_nin'),
    path('wallet/fund/', fund_wallet, name='fund_wallet'),
    # path("wallet/verify/<str:transaction_reference>/", verify_transaction, name="verify_transaction"),
    path('monnify/webhook/', monnify_webhook, name='monnify_webhook'),
    path('orders/', order_list, name='order_list'),
    path('purchase/<uuid:account_id>/', purchase_account, name='purchase_account'),
]
