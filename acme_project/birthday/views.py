from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


class BirthdayListView(LoginRequiredMixin, ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayCreateView(LoginRequiredMixin, BirthdayMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form) 


class BirthdayUpdateView(LoginRequiredMixin, BirthdayMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(LoginRequiredMixin, BirthdayMixin, DeleteView):
    model = Birthday
    pass


class BirthdayDetailView(LoginRequiredMixin, DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context
