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
from django.conf import settings

logger = logging.getLogger(__name__)

@login_required
def wallet_view(request):
    """Redirects user to fund wallet if NIN is needed."""
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    return render(request, "payments/wallet.html", {"wallet": wallet})


@login_required
def fund_wallet(request):
    """Handles both NIN submission and showing the virtual account."""
    user = request.user
    wallet, _ = Wallet.objects.get_or_create(user=user)

    if wallet.virtual_account_number:
        # If the virtual account exists, show the details
        return render(request, "payments/fund_wallet.html", {
            "account_number": wallet.virtual_account_number,
            "bank_name": wallet.bank_name,
            "account_name": user.get_full_name() or "Logs Place User",
        })

    # If no virtual account, request NIN
    if request.method == "POST":
        form = NINForm(request.POST)
        if form.is_valid():
            wallet.nin = form.cleaned_data["nin"]
            wallet.save()

            # Generate virtual account
            monnify = MonnifyService()
            response = monnify.get_or_create_reserved_account(user)

            if "error" in response:
                messages.error(request, "Failed to generate account. Try again.")
                return redirect("fund_wallet")

            account_details = response.get("responseBody", {})

            if not account_details.get("accountNumber"):
                messages.error(request, "Invalid response from Monnify. Try again.")
                return redirect("fund_wallet")

            wallet.virtual_account_number = account_details["accountNumber"]
            wallet.bank_name = account_details["bankName"]
            wallet.save()

            messages.success(request, "Your virtual account has been created!")
            return redirect("fund_wallet")  # Reload to show account details
    else:
        form = NINForm()

    return render(request, "payments/fund_wallet.html", {"form": form})


@login_required
def verify_transaction(request, transaction_reference):
    """Verify a Monnify transaction and update wallet balance."""
    monnify = MonnifyService()
    response = monnify.verify_transaction(transaction_reference)

    if "error" in response:
        return JsonResponse({"error": response["error"]}, status=400)

    transaction_data = response["responseBody"]

    if transaction_data["paymentStatus"] == "PAID":
        wallet = Wallet.objects.get(user=request.user)
        amount = float(transaction_data["amountPaid"])
        wallet.balance += amount
        wallet.save()

        MonnifyTransaction.objects.create(
            user=request.user,
            transaction_reference=transaction_reference,
            amount=amount,
            status="PAID"
        )

        return JsonResponse({"message": "Wallet funded successfully!"})

    return JsonResponse({"error": "Payment not completed"}, status=400)

@csrf_exempt
def monnify_webhook(request):
    """Handle Monnify webhook notifications."""
    try:
        payload = json.loads(request.body)
        logger.info(f"Monnify Webhook Data: {payload}")

        if payload.get("eventType") == "SUCCESSFUL_TRANSACTION":
            transaction_reference = payload["eventData"]["transactionReference"]
            amount_paid = float(payload["eventData"]["amountPaid"])
            account_reference = payload["eventData"]["accountReference"]

            wallet = Wallet.objects.get(user__id=account_reference)
            wallet.balance += amount_paid
            wallet.save()

            MonnifyTransaction.objects.create(
                user=wallet.user,
                transaction_reference=transaction_reference,
                amount=amount_paid,
                status="PAID"
            )

            return JsonResponse({"message": "Wallet updated successfully!"})

    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return JsonResponse({"error": "Webhook processing failed"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

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
            order.mark_as_paid()
            messages.success(request, "Purchase successful! Check your email for details.")
        except ValueError:
            messages.error(request, "Something went wrong. Please try again.")
            return redirect("wallet_view")

        return redirect(reverse("payments:order_list"))

    messages.error(request, "Insufficient balance. Please fund your wallet.")
    return redirect("wallet_view")
