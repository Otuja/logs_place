from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import SocialAccount
from .forms import SocialAccountForm



def index(request):
    return render(request, 'products/index.html')


# Check if the user is an admin
def is_admin(user):
    return user.is_superuser


@login_required
def social_accounts_list(request):
    accounts = SocialAccount.objects.filter(is_sold=False)  # Show only available accounts
    return render(request, 'products/social_accounts_list.html', {'accounts': accounts})


@login_required
def filter_social_accounts(request):
    """Filters social accounts based on query parameters"""
    platform = request.GET.get('platform', '')  # Get platform from URL query
    is_verified = request.GET.get('is_verified', '')  
    is_sold = request.GET.get('is_sold', '')

    accounts = SocialAccount.objects.all()

    if platform:
        accounts = accounts.filter(platform=platform)

    if is_verified:
        accounts = accounts.filter(is_verified=is_verified.lower() == 'true')

    if is_sold:
        accounts = accounts.filter(is_sold=is_sold.lower() == 'true')

    return render(request, 'products/social_accounts_list.html', {'accounts': accounts})



# Admin-Only: Create Social Account
@login_required
@user_passes_test(is_admin)  # Only superusers can access this view
def add_social_account(request):
    """Add a new social account"""
    if request.method == "POST":
        form = SocialAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:social_accounts_list')
    else:
        form = SocialAccountForm()
    
    return render(request, 'products/add_social_account.html', {'form': form})

@login_required
def social_account_detail(request, pk):
    """Displays details of a single social account"""
    account = get_object_or_404(SocialAccount, pk=pk)
    return render(request, 'products/social_account_detail.html', {'account': account})


# Admin-Only: Create Social Account
@login_required
@user_passes_test(is_admin)  # Only superusers can access this view
def update_social_account(request, pk):
    """Update an existing social account"""
    account = get_object_or_404(SocialAccount, pk=pk)
    if request.method == "POST":
        form = SocialAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('products:social_accounts_list')
    else:
        form = SocialAccountForm(instance=account)
    
    return render(request, 'products/update_social_account.html', {'form': form})


# Admin-Only: Create Social Account
@login_required
@user_passes_test(is_admin)  # Only superusers can access this view
def delete_social_account(request, pk):
    """Delete a social account"""
    account = get_object_or_404(SocialAccount, pk=pk)
    if request.method == "POST":
        account.delete()
        return redirect('products:social_accounts_list')
    
    return render(request, 'products/delete_social_account.html', {'account': account})



