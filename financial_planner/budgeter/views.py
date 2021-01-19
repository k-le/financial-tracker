from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import DeleteView, ListView
from .models import TransactionList, Transaction
from .forms import CreateNewList, CreateNewTransaction


def home(request):
    if request.user.is_authenticated:
        t_list = request.user.transactionlist.first()
        if t_list:
            return redirect("/dashboard/%i" % t_list.id + "?id=%i" % t_list.id)
        else:
            return redirect("budgeter-create")

    return render(request, 'budgeter/home.html')


def create(request):
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

        return render(request, "budgeter/create.html", {"form": form})

    return render(request, "budgeter/error.html", {'title': '404 Error'})


def dashboard(request, id):
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

        ingoing_sum: float = t_list.transaction.all().aggregate(in_sum=Sum('ingoing'))['in_sum']
        outgoing_sum: float = t_list.transaction.all().aggregate(out_sum=Sum('outgoing'))['out_sum']
        total_bal: float = ingoing_sum - outgoing_sum

        context = {'title': 'My Dashboard',
                   'form': form,
                   'transactions': t_list.transaction.all().order_by('-date_posted'),
                   't_list': t_list,
                   'ingoing_sum': ingoing_sum,
                   'outgoing_sum': outgoing_sum,
                   'total_bal': total_bal
                   }

        return render(request, 'budgeter/dashboard.html', context)

    return render(request, 'budgeter/error.html', {'title': '404 Error'})


class TransactionListListView(LoginRequiredMixin, ListView):
    model = TransactionList
    template_name = 'budgeter/budget_list.html'
    context_object_name = 'transaction_lists'
    ordering = ['name']


class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    success_url = '/'

    def test_func(self):
        return True
