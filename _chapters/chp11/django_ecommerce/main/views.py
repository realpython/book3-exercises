from django.shortcuts import render_to_response
from payments.models import User


def index(request):
    uid = request.session.get('user')
    if uid is None:
        return render_to_response('main/index.html')
    else:
        return render_to_response(
            'main/user.html', {'user': User.get_by_id(uid)}
        )
