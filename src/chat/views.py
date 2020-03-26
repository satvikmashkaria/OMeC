from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView

from .forms import ComposeForm
from .models import Thread, ChatMessage
import datetime
from django.utils import timezone


class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    context_object_name = 'old_threads'
    def get_queryset(self):
        Thread_list = Thread.objects.by_user(self.request.user)
        # if Thread_list[0].updated < timezone.now():
        #     print("It workedddd!")
        # print("Threadd: ", Thread_list[0].timestamp, datetime.datetime.now())
        old_threads = []
        for thread in Thread_list:
            if self.check_new(thread):
                old_threads.append(thread)
        return old_threads

    def get_context_data(self, *args, **kwargs):
        context = super(InboxView, self).get_context_data(*args, **kwargs)
        Thread_list = Thread.objects.by_user(self.request.user)
        
        new_threads = []
        for thread in Thread_list:
            if not self.check_new(thread):
                new_threads.append(thread)
        context['new_threads'] = new_threads
        return context 

    def check_new(self, thread):
        if thread.first.username == self.request.user.username:
            if thread.seen_by_first == 'y':
                return True
            else:
                return False
        if thread.second.username == self.request.user.username:
            if thread.seen_by_second == 'y':
                return True
            else:
                return False
        


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        print("yttoooot", other_username)
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)


