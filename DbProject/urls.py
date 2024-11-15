from django.contrib import admin
from django.urls import path
from loginreg import views
from forum import views as forumview
from Society import views as sviews

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
]
