from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required



from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # redirect to your main view after login
    else:
        form = UserCreationForm()
    return render(request, 'expenses/signup.html', {'form': form})


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)  # Don't save yet
            expense.user = request.user  # Assign the logged-in user
            expense.save()  # Now save the expense
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

from .expense_analysis import expense_trend_analysis, category_spending_analysis, clustering_expenses
from django.shortcuts import render
@login_required
def expense_analysis(request):
    # Run the analysis functions
    expense_trend_analysis()  # You can modify these to return data or graphs if necessary
    category_spending_analysis()
    # clustering_expenses()

    return render(request, 'expenses/expense_analysis.html')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense

def delete_expense(request, expense_id):
    # Get the expense object by its id
    expense = get_object_or_404(Expense, id=expense_id)
    
    # Delete the expense object
    expense.delete()
    
    # Redirect back to the expense list page
    return redirect('expense_list')


import plotly.express as px
import pandas as pd
from django.shortcuts import render
from .models import Expense
@login_required
def expense_analysis(request):
    # Retrieve all expenses from the database
    expenses = Expense.objects.all()

    # Prepare the data for the graph (categorizing and summing amounts)
    data = {
        "Category": [],
        "Amount": [],
    }

    # Loop through all expenses and aggregate the amounts by category
    for expense in expenses:
        data["Category"].append(expense.category)
        data["Amount"].append(expense.amount)

    # Create a dataframe from the data
    df = pd.DataFrame(data)

    # Create a bar chart showing total spending per category
    bar_chart = px.bar(df, x="Category", y="Amount", title="Spending by Category", labels={"Amount": "Amount Spent"})
    
    # Create a pie chart showing the distribution of spending per category
    pie_chart = px.pie(df, names="Category", values="Amount", title="Spending Distribution")

    # Convert the charts to HTML
    bar_chart_html = bar_chart.to_html(full_html=False)
    pie_chart_html = pie_chart.to_html(full_html=False)

    # Render the page with the graphs
    return render(request, 'expenses/expense_analysis.html', {
        'bar_chart': bar_chart_html,
        'pie_chart': pie_chart_html,
    })

