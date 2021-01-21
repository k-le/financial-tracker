from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Transaction, TransactionList


class CreateNewList(forms.ModelForm):
    """Form for the User to create a new TransactionList.
    """

    class Meta:
        model = TransactionList
        fields = ('name',
                  'starting_balance'
                  )

        labels = {
            'name': _('Name of Budget'),
            'starting_balance': _('Starting Balance')
        }


class CreateNewTransaction(forms.ModelForm):
    """Form for the User to create a new Transaction.
    Features a Date-picker for the date_posted field.
    """

    class Meta:
        model = Transaction
        fields = ('date_posted',
                  'payee',
                  'memo',
                  'ingoing',
                  'outgoing'
                  )

        labels = {
            'date_posted': _('Date of Transaction'),
            'payee': _('Payee'),
            'memo': _('Memo'),
            'ingoing': _('Ingoing'),
            'outgoing': _('Outgoing')
        }

        widgets = {
            'date_posted': forms.DateTimeInput(attrs={'class': 'datepicker'})
        }
