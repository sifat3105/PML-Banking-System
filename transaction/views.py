from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from accounts.models import Account
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Transaction

# Create your views here.

@login_required
def home_view(request):
    user = request.user
    try:
        account = Account.objects.get(user=user)
    except Account.DoesNotExist:
        account = None  
    
    return render(request, 'home.html', {'account': account})
@login_required
def account_details(request):
    user = request.user
    try:
        account = Account.objects.get(user=user)
    except Account.DoesNotExist:
        account = None  
    return render(request, 'account_details.html',{'user':user,'account':account})
@login_required
def account_deposit(request):
    if request.method=="POST":
        amount = int(request.POST.get('amount', 0)) 
        description = request.POST.get('description')
        account = Account.objects.get(user=request.user)
        account.balance+=amount
        account.save()
        t=Transaction.objects.create(account=account,amount=amount)
        t.description=description
        t.transaction_type='deposit'
        t.save()
    return render(request, 'deposit.html')
@login_required
def account_withdraw(request):
    if request.method=="POST":
        amount = int(request.POST.get('amount', 0)) 
        description = request.POST.get('description')
        account = Account.objects.get(user=request.user)
        if not account.balance>=amount:
            return render(request, 'withdraw.html',{'error':'ininsufficient balance'})
        else:
            account.balance-=amount
            account.save()
            amount= -amount
            t=Transaction.objects.create(account=account,amount=amount)
            t.description=description
            t.transaction_type='withdrawal'
            t.save()
    return render(request, 'withdraw.html')


@login_required
def account_transfer(request):
    if request.method=="POST":
        recipient = int(request.POST.get('recipient'))
        recipient_account=get_object_or_404(Account,account_number=recipient )
        if recipient_account is None:
            return render(request, 'withdraw.html',{'error':'Recipient Account is not Found'})
        amount = int(request.POST.get('amount', 0))
        description = request.POST.get('description')
        account = Account.objects.get(user=request.user)
        if not account.balance>=amount:
            return render(request, 'withdraw.html',{'error':'ininsufficient balance'})
        else:
            account.balance-=amount
            account.save()
            t=Transaction.objects.create(account=account,amount=-amount)
            t.description=description
            t.transaction_type='transfer'
            t.save()
            recipient_account.balance+=amount
            recipient_account.save()
            r=Transaction.objects.create(account=recipient_account,amount=amount)
            r.description=description
            r.transaction_type='received'
            r.save()

    return render(request, 'transfer.html')



def account_transactions(request):
    account = Account.objects.get(user=request.user)
    transactions_list = Transaction.objects.filter(account=account).order_by('-timestamp')
    
    transaction_type = request.GET.get('type')
    if transaction_type:
        transactions_list = transactions_list.filter(transaction_type=transaction_type)
    
    paginator = Paginator(transactions_list, 10) 
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    
    return render(request, 'transactions.html', {'transactions': transactions})