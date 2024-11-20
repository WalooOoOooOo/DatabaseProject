from django.shortcuts import render, redirect, get_object_or_404
from .models import Society, MembershipRequest, Announcement, Event
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import MembershipApplicationForm,AnnouncementForm,EventForm
from django.urls import reverse
from loginreg.models import CustomUser
from django.http import JsonResponse


def pcom_page(request):
    society = Society.objects.filter(name__iexact="Procom").first()

    if not society:
        return render(request, '404.html', status=404)  

    is_member = society.members.filter(id=request.user.id).exists()
    is_admin = society.admins.filter(id=request.user.id).exists()
    show_announcements = is_member or is_admin

    context = {
    'society': society,
    'is_member': is_member,
    'is_admin': is_admin,
    'show_announcements': show_announcements,
    'apply_membership_url': reverse('aform', args=[society.id]),
    }
    return render(request,'pcom_page.html',context)

def acm_page(request):
    society = Society.objects.filter(name__iexact="AMCS").first()

    if not society:
        return render(request, '404.html', status=404)  

    is_member = society.members.filter(id=request.user.id).exists()
    is_admin = society.admins.filter(id=request.user.id).exists()
    show_announcements = is_member or is_admin

    context = {
    'society': society,
    'is_member': is_member,
    'is_admin': is_admin,
    'show_announcements': show_announcements,
    'apply_membership_url': reverse('aform', args=[society.id]),
    }
    return render(request,'acm_page.html',context)

@login_required
@login_required
def upcoming_events(request, society_id):
    society = get_object_or_404(Society, id=society_id)
    events = Event.objects.filter(society=society).order_by('date')
    is_admin = society.admins.filter(id=request.user.id).exists()

    context = {
        'society': society,
        'events': events,
        'is_admin': is_admin,
    }
    return render(request, 'upcoming_events.html', context)


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

   
    is_admin = event.society.admins.filter(id=user.id).exists()

    if request.method == 'POST' and event.is_participating_event and not is_admin:
        if event.remaining_slots() > 0:
            event.participants.add(user)
        else:
            return render(request, 'event_detail.html', {'event': event, 'error': 'No slots available', 'is_admin': is_admin})

    context = {
        'event': event,
        'can_participate': event.is_participating_event and user not in event.participants.all() and not is_admin,
        'remaining_slots': event.remaining_slots(),
        'is_admin': is_admin,
    }
    return render(request, 'event_detail.html', context)



@login_required
def create_event(request, society_id):
    society = get_object_or_404(Society, id=society_id)

    if not society.admins.filter(id=request.user.id).exists():
        return redirect('decshome')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)  
        if form.is_valid():
            event = form.save(commit=False)
            event.society = society
            event.created_by = request.user
            event.save()
            return redirect('upcoming_events', society_id=society.id)
    else:
        form = EventForm()

    context = {
        'form': form,
        'society': society,
    }
    return render(request, 'create_event.html', context)


@login_required
def announcements_page(request, society_id):
    society = get_object_or_404(Society, id=society_id)

    is_member = society.members.filter(id=request.user.id).exists()
    is_admin = society.admins.filter(id=request.user.id).exists()

    if is_admin:
        announcements = Announcement.objects.filter(society=society)
    elif is_member:
        announcements = Announcement.objects.filter(society=society, is_member_specific__in=[False, True])
    else:
        announcements = Announcement.objects.filter(society=society, is_member_specific=False)

    context = {
        "announcements": announcements,
        "society": society,
        "is_admin": is_admin,
    }
    return render(request, "announcements_page.html", context)


@login_required
def create_announcement(request, society_id):
    society = get_object_or_404(Society, id=society_id)

    if not society.admins.filter(id=request.user.id).exists():
        return redirect('decshome')  

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.society = society
            announcement.created_by = request.user
            announcement.save()
            return redirect('apanel')  
    else:
        form = AnnouncementForm()

    context = {
        'form': form,
        'society': society,
    }
    return render(request, 'create_announcement.html', context)

@login_required
def decs_page(request):
    society = Society.objects.filter(name__iexact="DECS").first()

    if not society:
        return render(request, '404.html', status=404)  

    is_member = society.members.filter(id=request.user.id).exists()
    is_admin = society.admins.filter(id=request.user.id).exists()
    show_announcements = is_member or is_admin

    context = {
    'society': society,
    'is_member': is_member,
    'is_admin': is_admin,
    'show_announcements': show_announcements,
    'apply_membership_url': reverse('aform', args=[society.id]),
    }
    return render(request, 'decpage.html', context)




@login_required
@login_required
def admin_panel(request):
    user_societies = Society.objects.filter(admins=request.user)
    current_society = user_societies.first()  

    if not current_society:
        return render(request, 'home')

    pending_requests = MembershipRequest.objects.filter(society=current_society, status='pending')
    announcements = current_society.announcements.all()
    events = current_society.events.all()
    members = current_society.members.all()
    admins = current_society.admins.all()

    event_participation = [
        {
            'event': event,
            'participants_count': event.participants.count(),
            'remaining_slots': event.remaining_slots(),
        }
        for event in events
    ]

    context = {
        'current_society': current_society,
        'pending_requests': pending_requests,
        'announcements': announcements,
        'event_participation': event_participation,
        'members': members,
        'admins': admins,
    }
    return render(request, 'admin_panel.html', context)


@login_required
def view_membership_request(request, request_id):
    membership_request = get_object_or_404(
        MembershipRequest, 
        id=request_id, 
        society__admins=request.user
    )
    
    if membership_request.society not in Society.objects.filter(admins=request.user):
        return redirect('admin_panel')

    context = {
        'membership_request': membership_request,
    }
    return render(request, 'membership_request_detail.html', context)

@login_required
def apply_membership(request, society_id):
    society = get_object_or_404(Society, id=society_id)

    if MembershipRequest.objects.filter(user=request.user, society=society, status='pending').exists():
        return render(request,'alreadypending.html')

    if request.method == 'POST':
        form = MembershipApplicationForm(request.POST, request.FILES)
        if form.is_valid():
           
            application = form.save(commit=False)
            application.user = request.user
            application.society = society
            application.save()

           
            MembershipRequest.objects.create(
                user=request.user,
                society=society,
                application=application,
                status='pending'
            )

            return redirect('decshome')  
    else:
        form = MembershipApplicationForm()

    return render(request, 'apply_membership.html', {'form': form, 'society': society})


@login_required
@require_POST
def approve_membership(request, request_id):
    membership_request = get_object_or_404(MembershipRequest, id=request_id, society__admins=request.user)
    membership_request.status = 'approved'
    membership_request.application.status = 'approved'
    membership_request.application.save()
    membership_request.society.members.add(membership_request.user)
    membership_request.save()
    return redirect('apanel')

@login_required
@require_POST
def reject_membership(request, request_id):
    membership_request = get_object_or_404(MembershipRequest, id=request_id, society__admins=request.user)
    membership_request.status = 'rejected'
    membership_request.application.status = 'rejected'
    membership_request.application.save()
    membership_request.save()
    return redirect('apanel')

