from django.shortcuts import render_to_response
from payments.models import User
from main.models import Marketing_items

def index(request):
    uid = request.session.get('user')
    market_items = Marketing_items.objects.all()
    if uid is None:
        return render_to_response('main/index.html',
                                  {'marketing_items':market_items})
    else:
        return render_to_response('main/user.html',
                                  {'marketing_items':market_items, 
                                   'user': User.get_by_id(uid)}
                                 )
