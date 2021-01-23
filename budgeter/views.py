from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import DeleteView, ListView
from .models import TransactionList, Transaction
from .forms import CreateNewList, CreateNewTransaction


def home(request):
    """If the User is already logged in, then Home-view will
    redirect the user to either:
        their dashboard if they have already created a budget.
        the Budgeter-create page to create their first budget.

    Otherwise, the Home-view will render the home.html template.
    """

    if request.user.is_authenticated:
        t_list = request.user.transactionlist.first()
        if t_list:
            return redirect("/dashboard/%i" % t_list.id + "?id=%i" % t_list.id)
        else:
            return redirect("budgeter-create")

    return render(request, 'budgeter/home.html')


def create(request):
    """Requires the User to be logged-in to access Create-view.
    Renders a form for the User to create a new budget and saves
    their starting balance as the initial transaction in the new
    budget.

    If the User is not logged-in, then the view renders a custom 404
    Error page.

    Variables passed through to the template:
        title: :class:`String`
            Title of the view.
        form: :class:`form`
            Rendered TransactionList form for the User.
    """

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateNewList(request.POST)

            if form.is_valid():
                name = form.cleaned_data["name"]
                s_balance = form.cleaned_data["starting_balance"]
                t_list = TransactionList(name=name, starting_balance=s_balance)
                t_list.save()
                request.user.transactionlist.add(t_list)

                date = timezone.now()
                payee = "Starting Balance"
                ingoing = form.cleaned_data["starting_balance"]

                s_transaction = Transaction(t_list=t_list,
                                            date_posted=date,
                                            payee=payee,
                                            memo="",
                                            ingoing=ingoing,
                                            outgoing=0.00,
                                            )
                s_transaction.save()

                return redirect("/dashboard/%i" % t_list.id + "?id=%i" % t_list.id)
        else:
            form = CreateNewList()

        return render(request, "budgeter/create.html", {"form": form, "title": "Create a New Budget"})

    return render(request, "budgeter/error.html", {'title': '404 Error'})


def dashboard(request, id):
    """Dashboard-view renders the dashboard template with
    the User's chosen TransactionList. The view renders a form
    for the User to enter and save new Transactions into their
    TransactionList.

    If the User is not logged-in, then the view renders a custom 404
    Error page.

    Variables passed through to the template:
        title: :class:`String`
            Title of the view.
        form: :class:`form`
            Rendered Transaction form for the User.
        transactions: :class:`Model Transaction`
            Transactions of the TransactionList to be rendered in
            the template.
        t_list: :class:`Model TransactionList`
            TransactionList that contains Transactions to be rendered
            in the template.
        ingoing_sum: :class:`Float`
            Sum of all the ingoing values across every Transaction.
        outgoing_sum: :class:`Float`
            Sum of all the outgoing values across every Transaction.
        total_bal: :class:`Float`
            The current, total balance by subtracting the ingoing_sum
            and the out_going sum.
    """

    t_list = TransactionList.objects.get(id=id)

    if t_list in request.user.transactionlist.all():
        if request.method == 'POST':
            form = CreateNewTransaction(request.POST)

            if form.is_valid():
                date = form.cleaned_data["date_posted"]
                payee = form.cleaned_data["payee"]
                memo = form.cleaned_data["memo"]
                ingoing = form.cleaned_data["ingoing"]
                outgoing = form.cleaned_data["outgoing"]

                transaction = Transaction(t_list=t_list,
                                          date_posted=date,
                                          payee=payee,
                                          memo=memo,
                                          ingoing=ingoing,
                                          outgoing=outgoing
                                          )
                transaction.save()

                return redirect("/dashboard/%i" % t_list.id + "?id=%i" % t_list.id)
        else:
            form = CreateNewTransaction()

        context = {'title': 'My Dashboard',
                   'form': form,
                   'transactions': t_list.transaction.all().order_by('-date_posted'),
                   't_list': t_list
                   }

        # Aggregate values from Transactions
        if t_list.transaction.exists():
            ingoing_sum: float = t_list.transaction.all().aggregate(in_sum=Sum('ingoing'))['in_sum']
            outgoing_sum: float = t_list.transaction.all().aggregate(out_sum=Sum('outgoing'))['out_sum']
            total_bal: float = ingoing_sum - outgoing_sum

            context['ingoing_sum'] = ingoing_sum
            context['outgoing_sum'] = outgoing_sum
            context['total_bal'] = total_bal

        return render(request, 'budgeter/dashboard.html', context)

    return render(request, 'budgeter/error.html', {'title': '404 Error'})


class TransactionListListView(LoginRequiredMixin, ListView):
    """ListView for all of the TransactionLists. Allows the User
    to see all of their created budgets so that they may pick
    which one to edit.

    Currently a work in progress.
    """

    model = TransactionList
    template_name = 'budgeter/budget_list.html'
    context_object_name = 'transaction_lists'
    ordering = ['name']


class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """DeleteView for all the Transactions. Allows the User
    to delete Transactions from their TransactionLists.
    """

    model = Transaction
    success_url = '/'

    def test_func(self):
        return True
