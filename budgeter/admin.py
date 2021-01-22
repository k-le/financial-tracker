from django.contrib import admin
from .models import TransactionList, Transaction

admin.site.register(TransactionList)    # Allow admin-page to view all of
admin.site.register(Transaction)        # the TransactionLists and Transactions
