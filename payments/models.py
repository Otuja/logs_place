from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import uuid
from products.models import SocialAccount
from django.db.models.signals import post_save
from django.dispatch import receiver

def get_default_user():
    return get_user_model().objects.first().id

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # for virtual account
    virtual_account_number = models.CharField(max_length=20, blank=True, null=True)  #Store Monnify account
    bank_name = models.CharField(max_length=100, blank=True, null=True)  #Store bank name
    account_name = models.CharField(max_length=255, blank=True, null=True)  # Store account name

    nin = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.virtual_account_number if self.virtual_account_number else 'No Account'}"

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

# ✅ Automatically create a Wallet when a new User is created
@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)

class MonnifyTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_completed(self):
        """Mark the transaction as completed and deposit to user's wallet."""
        if self.status != 'completed':  # ✅ Prevent duplicate deposits
            self.status = 'completed'
            self.save()
            
            wallet = Wallet.objects.get(user=self.user)  # ✅ Ensure correct lookup
            wallet.deposit(self.amount)

class Order(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE)
    transaction = models.OneToOneField(MonnifyTransaction, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.account.username} - {self.status}"

    def mark_as_paid(self):
        """ Deduct from wallet and mark as paid """
        if self.user.wallet.withdraw(self.account.price):
            self.status = 'paid'
            self.account.is_sold = True  # ✅ Mark the account as sold
            self.account.save()
            self.save()
            
            # ✅ Send credentials to the buyer
            self.send_credentials_email()
        else:
            raise ValueError("Insufficient balance")

    def send_credentials_email(self):
        """Send account credentials to the buyer after payment."""
        subject = f"Your {self.account.platform} Account Details"
        message = (
            f"Dear {self.user.username},\n\n"  # ✅ Use the buyer's username
            f"Thank you for your purchase!\n\n"
            f"Here are your account details:\n"
            f"Username: {self.account.username}\n"
            f"Email: {self.account.email}\n"
            f"Password: {self.account.password}\n\n"
            f"Please keep this information secure.\n\n"
            f"Best Regards,\n"
            f"LogsPlace Team"
        )
        send_mail(subject, message, 'jp9backup@gmail.com', [self.user.email])  # ✅ Send to registered email


