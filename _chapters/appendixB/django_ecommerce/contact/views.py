from django.http import HttpResponseRedirect
from .forms import ContactView
from django.contrib import messages
from django.shortcuts import render
from payments.models import User


def contact(request):
    if request.method == 'POST':
        form = ContactView(request.POST)
        if form.is_valid():
            our_form = form.save(commit=False)
            our_form.save()
            messages.add_message(
                request, messages.INFO, 'Your message has been sent. Thank you.'
            )
            return HttpResponseRedirect('/')
    else:
        form = ContactView()

    context = {'form': form}

    return render(
        request,
        'contact/contact.html',
        context,
    )


