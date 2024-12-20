from django.shortcuts import render, redirect, get_object_or_404
from .models import Society, MembershipRequest, Announcement, Event,ParticipationDetail,MembershipApplication
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import MembershipApplicationForm,AnnouncementForm,EventForm,ParticipationDetailForm
from django.urls import reverse
from loginreg.models import CustomUser
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from forum.models import Post, Comment
from .forms import ProfilePictureForm
from django.contrib import messages
from django.contrib.messages import get_messages
from django.db import connection

@login_required
def remove_member(request, society_id, user_id):
    society = get_object_or_404(Society, id=society_id)
    user_to_remove = get_object_or_404(CustomUser, id=user_id)
    if request.user not in society.admins.all():
        return HttpResponseRedirect(reverse('apanel'))
    society.members.remove(user_to_remove)
    return HttpResponseRedirect(reverse('apanel'))

@login_required
@require_POST
def delete_participant(request, event_id, participant_id):
    event = get_object_or_404(Event, id=event_id)
    participant = get_object_or_404(CustomUser, id=participant_id)

    if not event.society.admins.filter(id=request.user.id).exists():
        return redirect('home')

    event.participants.remove(participant)
    event.banned_participants.add(participant)

    messages.info(request, f"The participant '{participant.username}' has been removed and banned from the event '{event.title}'.")

    return redirect('event_participants', event_id=event_id)

@login_required
def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    societies = user.society_members.all()
    admin_societies = user.society_admins.all()
    participation_details = ParticipationDetail.objects.filter(participant=user)

    membership_applications = MembershipApplication.objects.filter(user=user)
    for application in membership_applications:
        if application.society in societies:
            application.status = "Accepted"  

    user_posts = Post.objects.filter(author=user).order_by('-created_at') 
    user_comments = Comment.objects.filter(author=user).order_by('-created_at')  

    if request.method == "POST" and request.user == user:
        form = ProfilePictureForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = ProfilePictureForm(instance=user) if request.user == user else None

    context = {
        "user": user,
        "societies": societies,
        "admin_societies": admin_societies,
        "participation_details": participation_details,
        "membership_applications": membership_applications,
        "user_posts": user_posts,  
        "user_comments": user_comments,  
        "form": form,
    }
    return render(request, "profile.html", context)




@login_required
def view_event_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not event.society.admins.filter(id=request.user.id).exists():
        return redirect('admin_panel.html')  
    participants = event.participants.all()  
    context = {
        'event': event,
        'participants': participants,
    }
    return render(request, 'event_participants.html', context)

@login_required
def add_participation_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if user in event.banned_participants.all():
        return render(request, 'event_detail.html', {
            'event': event,
            'error': "You have been removed from this event and cannot re-register."
        })

    if event.participants.filter(id=user.id).exists():
        return render(request, 'event_detail.html', {
            'event': event,
            'error': "You are already registered for this event."
        })

    if not event.is_participating_event:
        return redirect('event_detail', event_id=event.id)

    if request.method == 'POST':
        form = ParticipationDetailForm(request.POST)
        if form.is_valid():
            participation_detail = form.save(commit=False)
            participation_detail.event = event
            participation_detail.participant = user
            participation_detail.save()

            event.participants.add(user)
            return redirect('event_detail', event_id=event.id)
    else:
        form = ParticipationDetailForm()

    return render(request, 'add_participation_detail.html', {'form': form, 'event': event})



@login_required
@require_POST
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not event.society.admins.filter(id=request.user.id).exists():
        return redirect('home')  
    event.delete()
    return redirect('upcoming_events', society_id=event.society.id)


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not event.society.admins.filter(id=request.user.id).exists():
        return redirect('home')  
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form, 'event': event})


@login_required
@require_POST
def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    society = announcement.society

    if not society.admins.filter(id=request.user.id).exists():
        return redirect('announcements_page', society_id=society.id)

    announcement.delete()
    return redirect('announcements_page', society_id=society.id)


@login_required
def edit_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    society = announcement.society

    if not society.admins.filter(id=request.user.id).exists():
        return redirect('announcements_page', society_id=society.id)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcements_page', society_id=society.id)
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'edit_announcement.html', {'form': form, 'announcement': announcement})


@login_required
def pcom_page(request):
    society = Society.objects.filter(name__iexact="Procom").first()
    if not society:
        return render(request, '404.html', status=404)  
    is_in_any_society = Society.objects.filter(
        members=request.user
    ).exists() or Society.objects.filter(
        admins=request.user
    ).exists()
    is_member = society.members.filter(id=request.user.id).exists()
    is_admin = society.admins.filter(id=request.user.id).exists()
    context = {
        'society': society,
        'is_member': is_member,
        'is_admin': is_admin,
        'show_announcements': is_member or is_admin,
        'show_apply_button': not is_in_any_society and not is_member and not is_admin,
        'apply_membership_url': reverse('aform', args=[society.id]),
    }
    return render(request, 'pcom_page.html', context)

@login_required
def acm_page(request):
    society = Society.objects.filter(name__iexact="AMCS").first()

    if not society:
        return render(request, '404.html', status=404)  

    is_in_any_society = Society.objects.filter(
        members=request.user
    ).exists() or Society.objects.filter(
        admins=request.user
    ).exists()

    is_member = society.members.filter(id=request.user.id).exists()
    is_admin = society.admins.filter(id=request.user.id).exists()

    context = {
        'society': society,
        'is_member': is_member,
        'is_admin': is_admin,
        'show_announcements': is_member or is_admin,
        'show_apply_button': not is_in_any_society and not is_member and not is_admin,
        'apply_membership_url': reverse('aform', args=[society.id]),
    }
    return render(request, 'acm_page.html', context)

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

    storage = get_messages(request)
    user_message = None
    for message in storage:
        if "Your participation in the event" in str(message):
            user_message = str(message)
            break

    context = {
        'event': event,
        'can_participate': event.is_participating_event and user not in event.participants.all() and not is_admin,
        'remaining_slots': event.remaining_slots(),
        'is_admin': is_admin,
        'user_message': user_message,
    }
    return render(request, 'event_detail.html', context)



@login_required
def create_event(request, society_id):
    society = get_object_or_404(Society, id=society_id)

    if not society.admins.filter(id=request.user.id).exists():
        return redirect('home')

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

    is_in_any_society = Society.objects.filter(
        members=request.user
    ).exists() or Society.objects.filter(
        admins=request.user
    ).exists()
    is_member = society.members.filter(id=request.user.id).exists()
    is_admin = society.admins.filter(id=request.user.id).exists()
    context = {
        'society': society,
        'is_member': is_member,
        'is_admin': is_admin,
        'show_announcements': is_member or is_admin,
        'show_apply_button': not is_in_any_society and not is_member and not is_admin,
        'apply_membership_url': reverse('aform', args=[society.id]),
        'members': society.members.all(),  
        'admins': society.admins.all(),   
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

def apply_membership(request, society_id):
    society = get_object_or_404(Society, id=society_id)

    if MembershipRequest.objects.filter(user=request.user, society=society, status='pending').exists():
        return render(request, 'alreadypending.html', {'society': society})

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
            if society_id == 1:
                return redirect('decshome')
            elif society_id == 2:
                return redirect('acmhome')
            elif society_id == 3:
                return redirect('pcomhome')
            else:
                return redirect(reverse('society', kwargs={'society_id': society.id}))
    else:
        form = MembershipApplicationForm()

    return render(request, 'apply_membership.html', {'form': form, 'society': society})



@login_required
@require_POST
def approve_membership(request, request_id):
    membership_request = get_object_or_404(MembershipRequest, id=request_id)

    if request.user not in membership_request.society.admins.all():
        return HttpResponseRedirect(reverse('apanel'))  

    membership_request.status = 'approved'
    membership_request.save()
    membership_request.society.members.add(membership_request.user)

    MembershipApplication.objects.filter(
        user=membership_request.user,
        status='pending'
    ).exclude(
        id=membership_request.application.id
    ).delete()

    messages.success(request, f"Membership approved for {membership_request.user.username}. Other applications have been removed.")
    return HttpResponseRedirect(reverse('apanel'))

@login_required
@require_POST
def reject_membership(request, request_id):
    membership_request = get_object_or_404(MembershipRequest, id=request_id, society__admins=request.user)
    membership_request.status = 'rejected'
    membership_request.application.status = 'rejected'
    membership_request.application.save()
    membership_request.save()
    return redirect('apanel')