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
        todos = Todo.objects.filter(title__icontains = query)
    if start_date:
        start_date = parse_date(start_date)
        if start_date:
            todos = Todo.objects.filter(~Q(status='done'),due_date__gte = start_date)
    if end_date:
        end_date = parse_date(end_date)
        if end_date:
            todos = Todo.objects.filter(~Q(status='done'),due_date__lte = end_date)
    return render(request, 'todo/Todos.html', {'todos': todos})
