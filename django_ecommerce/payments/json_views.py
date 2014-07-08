from payments.models import User, UnpaidUsers
from payments.forms import UserForm
from payments.views import Customer
from rest_framework.response import Response
from django.db import transaction
from django.db import IntegrityError
from rest_framework.decorators import api_view

@api_view(['POST'])
def post_user(request):
    form = UserForm(request.DATA)

    if form.is_valid():
        try:
            #update based on your billing method (subscription vs one time)
            customer = Customer.create("subscription",
              email = form.cleaned_data['email'],
              description = form.cleaned_data['name'],
              card = form.cleaned_data['stripe_token'],
              plan="gold",
            )
        except Exception as exp:
            form.addError(exp)
        
        cd = form.cleaned_data            
        try:
            with transaction.atomic():
                user = User.create(cd['name'], cd['email'], cd['password'],
                   cd['last_4_digits'])

                if customer:
                    user.stripe_id = customer.id
                    user.save()
                else:
                    UnpaidUsers(email=cd['email']).save()

        except IntegrityError:
            form.addError(cd['email'] + ' is already a member')
        else:
            request.session['user'] = user.pk
            resp = {"status":"ok","url":'/'}
            return Response(resp, content_type="application/json")

        resp = {"status":"fail","errors":form.non_field_errors()}
        return Response(resp) 
    else: #for not valid
        resp = {"status":"form-invalid","errors":form.errors}
        return Response(resp) 

