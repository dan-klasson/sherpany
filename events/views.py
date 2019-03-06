from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404

from datetime import datetime
from bootstrap_datepicker_plus import DatePickerInput
from events.models import Event, Attendance

class EventListView(ListView):
    queryset = Event.objects \
        .prefetch_related('attending') \
        .filter(date__gte=datetime.now()) \
        .order_by('-date')
    paginate_by = 20
    template_name = 'event_list.html'

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        # owners of the event should see the edit link
        if obj.user == self.request.user:
            context.update({'can_edit': True})
        # users already attending an event should not see the attend link
        if obj.attending.filter(user=self.request.user).exists():
            context.update({'already_attending': True})
        return context

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'date']
    template_name = 'event_form.html'
    success_url = reverse_lazy('event:list')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update events """
        if self.get_object().user != request.user:
            raise Http404
        return super(EventUpdateView, self).dispatch(request, *args, **kwargs)

class EventCreateView(LoginRequiredMixin, CreateView):
    """ authentication is required """
    model = Event
    fields = ['title', 'description', 'date']
    template_name = 'event_form.html'
    success_url = reverse_lazy('event:list')

    def get_form(self):
        """ override form to include date picker """
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        """ override form validation method to include current user """
        form.instance.user = self.request.user
        return super(EventCreateView, self).form_valid(form)

class AttendanceView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('event:list')

    def get_redirect_url(self, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs.get('pk'))
        attendance, created = Attendance.objects.get_or_create(
            user=self.request.user,
            event=event
        )
        return super().get_redirect_url(*args, **kwargs)