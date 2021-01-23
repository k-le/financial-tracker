from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone, dateformat


class TransactionList(models.Model):
    """List of transactions that is unique to each User so
    that they can manage and see their own transactions.

    Attributes
    ----------
    user: :class:`ForeignKey`
        User who created the transaction list. If the User has
        been deleted, then all of the transaction lists that were
        made by the User will be deleted.
    name: :class:`CharField`
        Name of the TransactionList.
    starting_balance: :class:`DecimalField`
        The starting balance (initial transaction) of the transaction
        list. This value is set by the User.
    """

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="transactionlist",
                             null=True)
    name = models.CharField(max_length=150)
    starting_balance = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Transactions that Users can create in their
    TransactionList.

    Attributes
    ----------
    t_list: :class:`ForeignKey`
        Every Transaction belongs to a TransactionList.
        Every TransactionList is unique to a User. This
        allows for Users to have multiple TransactionLists,
        each with different Transactions.
    date_posted: :class:`DateField`
        When the Transaction was made by the User. The
        default is the current date, but may be set
        by the User.
    payee: :class:`CharField`
        Payee of the Transaction. The User sets who the
        payee of the Transaction was.
    memo: :class:`TextField`
        Any notes that the User would like to leave for
        the Transaction.
    ingoing: :class:`DecimalField`
        The ingoing dollar value of the Transaction. Set to
        two decimal places for currency format.
    outgoing: :class:`DecimalField`
        The outgoing dollar value of the Transaction. Set
        to two decimal places for the currency format.
    """

    t_list = models.ForeignKey(TransactionList,
                               on_delete=models.CASCADE,
                               related_name='transaction',
                               null=True)
    date_posted = models.DateField(blank=False,
                                   default=dateformat.format(timezone.now(), 'm/d/y'))
    payee = models.CharField(max_length=100)
    memo = models.CharField(blank=True, max_length=300)
    ingoing = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    outgoing = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return f"User: {self.t_list.user}\n" \
               f"Budget: {self.t_list.name}\n" \
               f"Payee: {self.payee}\n" \
               f"Ingoing: ${self.ingoing}\n" \
               f"Outgoing: ${self.outgoing}"
