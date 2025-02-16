import json
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Wallet, MonnifyTransaction, Order
from products.models import SocialAccount
from .monnify_service import MonnifyService
from .forms import NINForm
from decimal import Decimal
# from django.conf import settings

logger = logging.getLogger(__name__)

@login_required
def wallet_view(request):
    """Redirects user to fund wallet if NIN is needed."""
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    return render(request, "payments/wallet.html", {"wallet": wallet})

@login_required
def submit_nin(request):
    """Handles NIN submission before creating a virtual account."""
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    
    if wallet.nin:  # If NIN is already provided, redirect to fund wallet
        return redirect("fund_wallet")
    
    if request.method == "POST":
        form = NINForm(request.POST)
        if form.is_valid():
            wallet.nin = form.cleaned_data["nin"]
            wallet.save()
            return redirect("fund_wallet")  # Proceed to create the virtual account
    else:
        form = NINForm()
    
    return render(request, "payments/submit_nin.html", {"form": form})


@login_required
def fund_wallet(request):
    """Displays or creates a virtual account for wallet funding."""
    user = request.user
    wallet, _ = Wallet.objects.get_or_create(user=user)

    if not wallet.nin:
        return redirect("submit_nin")  # Ensure user submits NIN first

    # ✅ Check if the virtual account already exists before creating a new one
    if not wallet.virtual_account_number:
        monnify = MonnifyService()
        response = monnify.create_reserved_account(user)

        if "error" in response:
            messages.error(request, response["error"])
            return redirect("wallet_view")

        # ✅ Store the virtual account details in the wallet
        wallet.virtual_account_number = response.get("accountNumber")
        wallet.bank_name = response.get("bankName")
        wallet.save()

    return render(request, "payments/fund_wallet.html", {
        "account_number": wallet.virtual_account_number,
        "bank_name": wallet.bank_name,
    })


# @login_required
# def verify_transaction(request, transaction_reference):
#     """Verify a Monnify transaction and update wallet balance."""
#     monnify = MonnifyService()
#     response = monnify.verify_transaction(transaction_reference)

#     if "error" in response:
#         return JsonResponse({"error": response["error"]}, status=400)

#     transaction_data = response["responseBody"]

#     if transaction_data["paymentStatus"] == "PAID":
#         wallet = Wallet.objects.get(user=request.user)
#         amount = float(transaction_data["amountPaid"])
#         wallet.balance += amount
#         wallet.save()

#         MonnifyTransaction.objects.create(
#             user=request.user,
#             transaction_reference=transaction_reference,
#             amount=amount,
#             status="PAID"
#         )

#         return JsonResponse({"message": "Wallet funded successfully!"})

#     return JsonResponse({"error": "Payment not completed"}, status=400)

@csrf_exempt
def monnify_webhook(request):
    """Handle Monnify webhook notifications."""
    try:
        payload = json.loads(request.body)
        logger.info(f"Monnify Webhook Data: {json.dumps(payload, indent=2)}")

        event_data = payload.get("eventData", {})  # Extract eventData

        # ✅ Extract transaction details
        transaction_reference = event_data.get("transactionReference")
        amount_paid = event_data.get("amountPaid")
        account_reference = event_data.get("product", {}).get("reference")  # Use product.reference

        if not all([transaction_reference, amount_paid, account_reference]):
            logger.error(f"Missing required webhook fields: {event_data}")
            return JsonResponse({"error": "Invalid webhook payload"}, status=400)

        # ✅ Ensure wallet exists for the provided accountReference
        wallet = Wallet.objects.filter(user__id=account_reference).first()
        if not wallet:
            logger.error(f"Wallet not found for user ID: {account_reference}")
            return JsonResponse({"error": "Wallet not found"}, status=400)

        # ✅ Update wallet balance
        wallet.balance += Decimal(str(amount_paid))
        wallet.save()

        # ✅ Save transaction
        MonnifyTransaction.objects.create(
            user=wallet.user,
            reference=transaction_reference,
            amount=amount_paid,
            status="completed"
        )

        logger.info(f"Wallet funded successfully for {wallet.user.username}")
        return JsonResponse({"message": "Wallet updated successfully!"})

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON received: {e}")
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return JsonResponse({"error": "Webhook processing failed"}, status=400)

    # return JsonResponse({"error": "Invalid request"}, status=400)




@login_required
def order_list(request):
    """List all orders for the user."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payments/order_list.html', {'orders': orders})

@login_required
def purchase_account(request, account_id):
    account = get_object_or_404(SocialAccount, id=account_id, is_sold=False)
    wallet = Wallet.objects.get(user=request.user)

    if wallet.balance >= account.price:
        order = Order.objects.create(user=request.user, account=account, status="pending")
        try:
            wallet.balance -= account.price  # Deduct balance
            wallet.save()
            order.mark_as_paid()
            messages.success(request, "Purchase successful! Check your email for details.")
        except ValueError:
            wallet.balance += account.price  # Rollback balance if error occurs
            wallet.save()
            messages.error(request, "Something went wrong. Please try again.")
            return redirect("wallet_view")

        return redirect(reverse("payments:order_list"))

    messages.error(request, "Insufficient balance. Please fund your wallet.")
    return redirect("wallet_view")

