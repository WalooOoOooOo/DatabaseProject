from django.contrib import admin
from django.urls import path
from loginreg import views
from forum import views as forumview
from Society import views as sviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignUpPage,name='signer'),
    path('login/',views.loginpage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('logout/',views.logoutpage,name='logout'),
    path('forum/',forumview.forum_page,name='forumhome'),
    path('forum/create',forumview.create_post,name='forumcreate'),
    path('forum/post/<int:post_id>/',forumview.post_detail,name='forumpostdetail'),
    path('adminpanel/',sviews.admin_panel,name='apanel'),
    path('approve-membership/<int:request_id>/', sviews.approve_membership, name='amember'),
    path('reject-membership/<int:request_id>/', sviews.reject_membership, name='rmember'),
    path('mdetails/',sviews.view_membership_request,name='mdetails'),
    path('decshome/', sviews.decs_page, name='decshome'),
    path('applymembership/<int:society_id>/', sviews.apply_membership, name='aform'),
    path('viewmemberships/<int:request_id>/', sviews.view_membership_request, name='viewmember'),
    path('approve-membership/<int:request_id>/', sviews.approve_membership, name='amember'), 
    path('reject-membership/<int:request_id>/', sviews.reject_membership, name='rmember'),  
    path('announcements/<int:society_id>/', sviews.announcements_page, name='announcements_page'),
    path('createannouncement/<int:society_id>/',sviews.create_announcement,name='create_announcement'),
   path('society/<int:society_id>/events/', sviews.upcoming_events, name='upcoming_events'),
    path('events/<int:event_id>/', sviews.event_detail, name='event_detail'), 
    path('society/<int:society_id>/events/new/', sviews.create_event, name='create_event'), 
    path('ACM/', sviews.acm_page, name='acmhome'),
    path('Procom/', sviews.pcom_page, name='pcomhome'),
    path('announcement/edit/<int:announcement_id>/', sviews.edit_announcement, name='edit_announcement'),
    path('announcement/delete/<int:announcement_id>/', sviews.delete_announcement, name='delete_announcement'),
    path('event/edit/<int:event_id>/', sviews.edit_event, name='edit_event'),
    path('event/delete/<int:event_id>/', sviews.delete_event, name='delete_event'),
    path('event/<int:event_id>/participation/', sviews.add_participation_detail, name='add_participation_detail'),
    path('event/<int:event_id>/participants/', sviews.view_event_participants, name='event_participants'),
    path('profile/<str:username>/', sviews.profile_view, name='user_profile'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('event/<int:event_id>/remove-participant/<int:participant_id>/', sviews.delete_participant, name='delete_participant'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)