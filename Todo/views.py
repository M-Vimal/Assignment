from datetime import datetime
from django.shortcuts import redirect, render
from .models import Todo
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.contrib import messages
# Create your views here.
def Home(request):
    todos = Todo.objects.all()
    context = {'todos':todos}
    return render(request,'todo/Todos.html',context)

def add(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['due_date'] and request.POST['status'] != '':
            title = request.POST['title']
            due_date = request.POST['due_date']
            status = request.POST['status']
            Todo.objects.create(
                title = title,
                due_date = due_date,
                status = status
            )
            return redirect('home')
        else:
            messages.error(request,"Form is not filled properly!!!")
    

    return render(request,'todo/add.html')

def delete(request,pk):
    delete_task = Todo.objects.get(id=pk)
    delete_task.delete()
    return redirect('home')

def todolist(request):
    query = request.GET.get('q')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    todos = Todo.objects.all()

    if query:
        query = query.lower()
        start_date, end_date = None, None
        query_filter = Q()

        # Extract date filters
        if " after " in query:
            parts = query.split(" after ")
            keywords = parts[0].strip()
            remaining_part = parts[1].strip()

            if " before " in remaining_part:
                remaining_parts = remaining_part.split(" before ")
                date_str_after = remaining_parts[0].strip()
                date_str_before = remaining_parts[1].strip()
                try:
                    start_date = datetime.strptime(date_str_after, "%d-%m-%Y").date()
                    end_date = datetime.strptime(date_str_before, "%d-%m-%Y").date()
                except ValueError:
                    print("Date format is incorrect. Please use dd-mm-yyyy.")
            else:
                date_str = remaining_part
                try:
                    start_date = datetime.strptime(date_str, "%d-%m-%Y").date()
                except ValueError:
                    print("Date format is incorrect. Please use dd-mm-yyyy.")
        elif " before " in query:
            parts = query.split(" before ")
            keywords = parts[0].strip()
            date_str = parts[1].strip()
            try:
                end_date = datetime.strptime(date_str, "%d-%m-%Y").date()
            except ValueError:
                print("Date format is incorrect. Please use dd-mm-yyyy.")
        else:
            keywords = query.strip()

        # Process keywords with "and" or "or"
        if " and " in keywords:
            keyword_list = [kw.strip() for kw in keywords.split(" and ")]
            for keyword in keyword_list:
                query_filter &= (
                    Q(title__iexact=keyword) |
                    Q(title__startswith=f'{keyword} ') |
                    Q(title__endswith=f' {keyword}') |
                    Q(title__icontains=f' {keyword} ')
                )
        elif " or " in keywords:
            keyword_list = [kw.strip() for kw in keywords.split(" or ")]
            for keyword in keyword_list:
                query_filter |= (
                    Q(title__iexact=keyword) |
                    Q(title__startswith=f'{keyword} ') |
                    Q(title__endswith=f' {keyword}') |
                    Q(title__icontains=f' {keyword} ')
                )
        else:
            # Single keyword
            query_filter = (
                Q(title__iexact=keywords) |
                Q(title__startswith=f'{keywords} ') |
                Q(title__endswith=f' {keywords}') |
                Q(title__icontains=f' {keywords} ')
            )

        # Apply keyword filter
        todos = todos.filter(query_filter)

        # Apply date filters
        if start_date:
            todos = todos.filter(due_date__gt=start_date)
        if end_date:
            todos = todos.filter(due_date__lt=end_date)

        
        
        elif " or " in query.lower():
            # Handle "or" logic
            words = query.lower().split(" or ")
            or_filter = Q()
            for word in words:
                or_filter |= (
                    Q(title__iexact=word) |
                    Q(title__startswith=f'{word} ') |
                    Q(title__endswith=f' {word}') |
                    Q(title__icontains=f' {word} ')
                )
            todos = todos.filter(or_filter)
        elif " and " in query.lower():
            words = query.lower().split(" and ")
            for word in words:
                todos = todos.filter(
                    Q(title__iexact=word) |
                    Q(title__startswith=f'{word} ') |
                    Q(title__endswith=f' {word}') |
                    Q(title__icontains=f' {word} ')
                )
        else:
            # Handle "and" logic (default case)
            words = query.split()
            for word in words:
                todos = todos.filter(
                    Q(title__iexact=word) |
                    Q(title__startswith=f'{word} ') |
                    Q(title__endswith=f' {word}') |
                    Q(title__icontains=f' {word} ')
                )
    if start_date:
        start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
        if start_date:
            todos = todos.filter(~Q(status='done'),due_date__gt = start_date)
    if end_date:
        end_date = datetime.strptime(end_date, "%d-%m-%Y").date()
        if end_date:
            todos = Todo.objects.filter(~Q(status='done'),due_date__lt = end_date)
    return render(request, 'todo/Todos.html', {'todos': todos})
    