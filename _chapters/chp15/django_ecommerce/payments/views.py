from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseBadRequest, \
    HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from payments.forms import SigninForm, CardForm, UserForm
from payments.models import User, UnpaidUsers
import django_ecommerce.settings as settings
import stripe
import datetime
import socket
import json

stripe.api_key = settings.STRIPE_SECRET


def soon():
    soon = datetime.date.today() + datetime.timedelta(days=30)
    return {'month': soon.month, 'year': soon.year}


def sign_in(request):
    user = None
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            results = User.objects.filter(email=form.cleaned_data['email'])
            if len(results) == 1:
                if results[0].check_password(form.cleaned_data['password']):
                    request.session['user'] = results[0].pk
                    return HttpResponseRedirect('/')
                else:
                    form.addError('Incorrect email address or password')
            else:
                form.addError('Incorrect email address or password')
    else:
        form = SigninForm()

    print(form.non_field_errors())

    return render_to_response(
        'payments/sign_in.html',
        {
            'form': form,
            'user': user
        },
        context_instance=RequestContext(request)
    )


def sign_out(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return HttpResponseRedirect('/')


def register(request):
    user = None
    if request.method == 'POST':
        # We only talk AJAX posts now
        if not request.is_ajax():
            return HttpResponseBadRequest("I only speak AJAX nowadays")

        data = json.loads(request.body.decode())
        form = UserForm(data)

        if form.is_valid():
            cd = form.cleaned_data
            from django.db import transaction
            try:
                with transaction.atomic():
                    user = User.create(cd['name'], cd['email'], cd['password'],
                                       cd['last_4_digits'], stripe_id="")

                    if customer:
                        user.stripe_id = customer.id
                        user.save()
                    else:
                        UnpaidUsers(email=cd['email']).save()
            except IntegrityError:
                form.addError(cd['email'] + ' is already a member')
            else:
                request.session['user'] = user.pk
                resp = json.dumps({"status": "ok", "url": '/'})
                return HttpResponse(resp, content_type="application/json")

            resp = json.dumps(
                {"status": "fail", "errors": form.non_field_errors()})
            return HttpResponse(resp, content_type="application/json")
        else:  # form not valid
            resp = json.dumps({"status": "form-invalid", "errors": form.errors})
            return HttpResponse(resp, content_type="application/json")

    else:
        form = UserForm()

    return render_to_response(
        'payments/register.html',
        {
            'form': form,
            'months': list(range(1, 12)),
            'publishable': settings.STRIPE_PUBLISHABLE,
            'soon': soon(),
            'user': user,
            'years': list(range(2011, 2036)),
        },
        context_instance=RequestContext(request)
    )


def edit(request):
    uid = request.session.get('user')

    if uid is None:
        return HttpResponseRedirect('/')

    user = User.objects.get(pk=uid)

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():

            customer = stripe.Customer.retrieve(user.stripe_id)
            customer.card = form.cleaned_data['stripe_token']
            customer.save()

            user.last_4_digits = form.cleaned_data['last_4_digits']
            user.stripe_id = customer.id
            user.save()

            return HttpResponseRedirect('/')

    else:
        form = CardForm()

    return render_to_response(
        'payments/edit.html',
        {
            'form': form,
            'publishable': settings.STRIPE_PUBLISHABLE,
            'soon': soon(),
            'months': list(range(1, 12)),
            'years': list(range(2011, 2036))
        },
        context_instance=RequestContext(request)
    )


class Customer(object):

    @classmethod
    def create(cls, billing_method="subscription", **kwargs):
        try:
            if billing_method == "subscription":
                return stripe.Customer.create(**kwargs)
            elif billing_method == "one_time":
                return stripe.Charge.create(**kwargs)
        except (socket.error, stripe.APIConnectionError,
                stripe.InvalidRequestError):
            return None
