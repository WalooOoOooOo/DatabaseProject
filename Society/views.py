from django.shortcuts import render, redirect, get_object_or_404
from .models import Society, MembershipRequest, Announcement, Event
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
def admin_panel(request):
    if not request.user.isadmin: 
        return redirect('home')

    user_societies = Society.objects.filter(admins=request.user)
    current_society = user_societies.first()  

    if not current_society:
        return render(request, 'home')

    pending_requests = MembershipRequest.objects.filter(society=current_society, status='pending')
    announcements = current_society.announcements.all()
    events = current_society.events.all()
    members = current_society.members.all()
    admins = current_society.admins.all()

    context = {
        'current_society': current_society,
        'pending_requests': pending_requests,
        'announcements': announcements,
        'events': events,
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
@require_POST
def approve_membership(request, request_id):
    membership_request = get_object_or_404(MembershipRequest, id=request_id, society__admins=request.user)
    membership_request.status = 'approved'
    membership_request.society.members.add(membership_request.user)
    membership_request.save()
    return redirect('admin_panel')

@login_required
@require_POST
def reject_membership(request, request_id):
    membership_request = get_object_or_404(MembershipRequest, id=request_id, society__admins=request.user)
    membership_request.status = 'rejected'
    membership_request.save()
    return redirect('admin_panel')