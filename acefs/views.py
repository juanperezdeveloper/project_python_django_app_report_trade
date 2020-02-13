from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.core.paginator import Paginator
from django_mlds.acefs.models import *
from django_mlds.acefs.acefs import *
import datetime
import hashlib
import base64
import time
import random
from django.contrib.admin.views.decorators import staff_member_required

def _hash_helper(input):
    h = hashlib.sha256()
    h.update(input)
    h.update(settings.SECRET)
    return h.hexdigest()


def _get_or_create_visitor(request):

    if request.GET.get('skip_log', False):
        return None

    user_agent = request.META['HTTP_USER_AGENT']

    bots = ['Pingdom.com_bot_']
    for b in bots:
        if user_agent.startswith(b):
            return None

    visitor = None
    try:
        visitor_id = request.session['visitor_id']
        visitor = Visitor.objects.get(pk=visitor_id)

    except Exception, e:
        visitor = Visitor()
        visitor.save()
        request.session['visitor_id']= visitor.id

    # Update IP and User-Agent
    visitor.ip = request.META.get('HTTP_X_REAL_IP', None) # Set by NGINX
    if not visitor.ip:
        visitor.ip = request.META['REMOTE_ADDR']
    visitor.user_agent = user_agent
    visitor.save()

    return visitor


def backdoor(request):

    visitor = _get_or_create_visitor(request)
    if visitor:
        visitor.username = '--'
        visitor.fullname = '(Backdoor User)'
        visitor.save()
    
    salt = str(random.randrange(10000,10000000))
    hash = _hash_helper(salt)

    response = HttpResponseRedirect('/')
    response.set_cookie('salt', salt, 365*24*60*60)
    response.set_cookie('hash', hash, 365*24*60*60)
    return response


def main(request):

    visitor = _get_or_create_visitor(request)

    if request.method == 'POST':

        # We might have a token from the other server:

        encoded = request.POST['encoded']
        hashed = request.POST['hashed']

        other_t = base64.b64decode(encoded)
        this_t = time.time()

        delta = abs(int(other_t) - this_t)

        this_hash = _hash_helper(other_t)

        if (delta > (60*60*2)) or (hashed != this_hash):

            return render_to_response('auth_error.html', {}, RequestContext(request))

        else:

            salt = str(random.randrange(10000,10000000))
            hash = _hash_helper(salt)

            # Save User Data to Session
            if visitor:
                visitor.modx_id = request.POST['id']
                visitor.username = request.POST['username']
                visitor.fullname = request.POST['fullname']
                visitor.save()

            response = HttpResponseRedirect('/')
            response.set_cookie('salt', salt, 365*24*60*60)
            response.set_cookie('hash', hash, 365*24*60*60)
            return response
    
    return render_to_response("index.html", {
        'colleges': College.objects.all().order_by('school'),
        'occupations': DOLSalary.objects.all().order_by('occupation'),
        'draft_cells': DRAFT_CELLS,
        'positions': POSITIONS,
        'statuses': STATUSES
        }, RequestContext(request))


def output(request):

    college = int(request.POST['college'])
    alt = int(request.POST['alt'])
    sec = int(request.POST['sec'])
    pick = int(request.POST['pick'])
    pos = int(request.POST['pos'])
    status = int(request.POST['status'])

    m = AcefsModel(college=college, alt=alt, secondary=sec, expected_pick=pick, position=pos, status=status)

    visitor = _get_or_create_visitor(request)
    if visitor:
        scenario = Scenario()
        scenario.visitor = visitor
        scenario.college = m.college
        scenario.alt = m.alt
        scenario.sec = m.secondary
        scenario.pick = m.expected_pick.cell
        scenario.pos = m.position.index
        scenario.status = m.status.index
        scenario.save()

    if request.COOKIES.has_key('salt'):

        # We might have a cookie:
        salt = request.COOKIES.get('salt', '')
        hash = request.COOKIES.get('hash', '')

        if (hash != _hash_helper(salt)):
            return render_to_response('auth_error.html', {}, RequestContext(request))

    else:

        return render_to_response('auth_error.html', {}, RequestContext(request))


    if visitor:
        scenario.anonymous = False
        scenario.save()

    table = []
    for y in range(0, TOTAL_YEARS):
        table.append({
            'year': y + datetime.datetime.now().year,
            'pr_minors': m.pr_minors[y],
            'pr_out': m.pr_out[y]
        })

    this_year = datetime.datetime.now().year
    graph = [
        {
            'label': 'Earnings [Baseball]',
            'data': [[y + this_year, m.e_mlb[y]] for y in range(0, TOTAL_YEARS)],
            'color': '#009900'
        },
        {
            'label': 'Earnings [Alternate]',
            'data': [[y + this_year, m.e_alt[y]] for y in range(0, TOTAL_YEARS)],
            'color': '#CC0000'
        }

        ]

    years = [this_year + 2 * y + 1 for y in range(0, TOTAL_YEARS/2)]

    return render_to_response('output.html', {
        'model': m,
        'table': table,
        'graph': graph,
        'years': years
    }, RequestContext(request))

@staff_member_required
def visitors(request):
    return render_to_response('visitors.html', {
    }, RequestContext(request))

@staff_member_required
def visitor_list(request, page_num=1):

    # Annotate using number of scenarios and filter to show only > 0
    visitors = Visitor.objects.annotate(num_scenarios=Count('scenario'))
    visitors = visitors.filter(num_scenarios__gt=0)
    
    if request.GET.has_key('term'):
        term = request.GET['term']
        visitors = visitors.filter(fullname__icontains=term)

    else:
        term = ''
        visitors = visitors.all()

    paginator = Paginator(visitors, 20)
    page = paginator.page(int(page_num))

    return render_to_response('visitor_list.html', {
        'term': term,
        'page': page
    }, RequestContext(request))

@staff_member_required
def visitor_detail(request, visitor_id):
    return render_to_response('visitor_detail.html', {
        'visitor': Visitor.objects.get(pk=visitor_id)
    }, RequestContext(request))
