# events/views.py
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Event, RSVP
from .forms import EventForm
from django.utils import timezone

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        # Show upcoming + ongoing events
        now = timezone.now()
        return Event.objects.filter(end_time__gte=now).order_by('start_time')


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        event = self.get_object()
        # If user is authenticated, check RSVP status
        rsvp = None
        if self.request.user.is_authenticated:
            try:
                rsvp = RSVP.objects.get(user=self.request.user, event=event)
            except RSVP.DoesNotExist:
                rsvp = None
        ctx['rsvp'] = rsvp
        return ctx


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, "✅ Event created successfully.")
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:list')

    def test_func(self):
        evt = self.get_object()
        return (self.request.user == evt.organizer) or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "⛔ You don't have permission to edit this event.")
        return redirect('events:detail', pk=self.get_object().pk)


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:list')

    def test_func(self):
        evt = self.get_object()
        return (self.request.user == evt.organizer) or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "⛔ You don't have permission to delete this event.")
        return redirect('events:detail', pk=self.get_object().pk)


class RSVPView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        # Create or update RSVP
        status = request.POST.get('status', RSVP.INTERESTED)
        rsvp, created = RSVP.objects.get_or_create(
            user=request.user, event=event, defaults={'status': status}
        )
        if not created:
            rsvp.status = status
            rsvp.save()
            messages.success(request, "✅ Your RSVP was updated.")
        else:
            messages.success(request, "✅ Your RSVP was recorded.")
        return redirect('events:detail', pk=pk)