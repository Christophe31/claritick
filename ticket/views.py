# -*- coding: utf-8 -*-

from django import http
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import escape
from django.contrib.auth.decorators import login_required

from claritick.ticket.models import Ticket
from claritick.ticket.forms import *
from claritick.ticket.tables import DefaultTicketTable

@login_required
def list_all(request, *args, **kw):
    """
    
    Liste tous les tickets sans aucun filtre
    """
    form = SearchTicketForm(request.POST)
    form.is_valid()
    
    qs = Ticket.objects.all()
    qs = qs.exclude(text=None)
    
    # Form cleaned_data ?
    try:
        print "form.cleaned_data %s" % (form.cleaned_data,)
        if form.cleaned_data:
            cd = form.cleaned_data
            for key, value in cd.items():
                if value:
                    qs = qs.filter(**{key:value})
    except AttributeError:
        pass
    table = DefaultTicketTable(data=qs, order_by=request.GET.get('sort', 'title'))
    
    return render_to_response('ticket/list.html', {'table': table, 'form': form }, context_instance=RequestContext(request))

@login_required
def partial_new(request, form=None):
    """
    Create a new ticket.
    """
    if not form:
        form = PartialNewTicketForm()
    return render_to_response('ticket/partial_new.html', {'form': form }, context_instance=RequestContext(request))

@login_required
def new(request):
    """
    Create a new ticket.
    """
    
    form = PartialNewTicketForm(request.POST)
    if not form.is_valid():
        return partial_new(request, form)
    
    ticket = form.save(commit=False)
    ticket.opened_by = request.user
    ticket.title = "Invalid title"
    ticket.state = None
    ticket.save()
    return redirect("/ticket/modify/%d" % (ticket.id,) )

@login_required
def modify(request, ticket_id):
    data = request.POST.copy()
    
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if not ticket.text:
        ticket.title = None
    
    if request.POST:
        form = NewTicketForm(request.POST, instance=ticket)
    else:
        form = NewTicketForm(instance=ticket)
    
    if data:
        print "data ! "
        if form.is_valid():
            print "form is_valid!"
            form.save()
        print form.errors

    return render_to_response("ticket/modify.html", {"form": form, "ticket": ticket}, context_instance=RequestContext(request))
