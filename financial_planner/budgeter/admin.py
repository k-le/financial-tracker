from django.contrib import admin
from .models import TransactionList, Transaction

admin.site.register(TransactionList)
admin.site.register(Transaction)
