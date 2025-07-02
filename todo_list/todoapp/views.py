from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ToDoList, ToDoItem
from django.shortcuts import render
from django.core.paginator import Paginator


def search_result_form(request):
    item_title = request.GET.get('item_title', '')

    if item_title:
        results = ToDoItem.objects.filter(title__icontains=item_title)
    else:
        results = ToDoItem.objects.all()

    paginator = Paginator(results, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'todo_app/todo_search_form.html', {'item_title': item_title, 'page_obj': page_obj})


class ListListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"
    

class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context


class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]
    template_name = "todo_app/todo_list_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add a new list"
        return context
        

class ItemCreate(CreateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]
    template_name = "todo_app/todo_item_form.html"

    def get_initial(self):
        initial = super().get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial["todo_list"] = todo_list
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse_lazy("list", args=[self.object.todo_list_id])


class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]
    template_name = "todo_app/todo_item_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse_lazy("list", args=[self.object.todo_list_id])


class ListDelete(DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index")
    template_name = "todo_app/todo_list_confirm_delete.html"


class ItemDelete(DeleteView):
    model = ToDoItem
    template_name = "todo_app/todo_item_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context
