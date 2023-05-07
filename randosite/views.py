from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse


def redir(request):
    return redirect('imageboard/')


def profile_view(request):
    return HttpResponseRedirect(reverse('imageboard:index'))