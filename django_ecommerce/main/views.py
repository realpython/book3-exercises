from django.shortcuts import render_to_response
from payments.models import User
from main.models import MarketingItem, StatusReport 
from django.template import RequestContext

def index(request):
    uid = request.session.get('user')
    if uid is None:
        #main landing page
        market_items = MarketingItem.objects.all()
        return render_to_response('main/index.html',
                                  {'marketing_items':market_items})
    else:
        #membership page
        status = StatusReport.objects.all().order_by('-when')[:20]
        return render_to_response('main/user.html',
                                  {'user': User.get_by_id(uid),
                                   'reports':status},
                                  context_instance=RequestContext(request),
                                 )
def report(request):
    if request.method == "POST":
        status = request.POST.get("status", "")
        #update the database with the status
        if status:
            uid = request.session.get('user')
            user = User.get_by_id(uid)
            StatusReports(user=user, status=status).save()
       
        #always return something
        return index(request)
