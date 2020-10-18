__author__ = 'PRIYANSH KHANDELWAL'

from rest_framework.routers import DefaultRouter
from nsp_project_app import views
router=DefaultRouter()
router.register(r'Client_views',views.client_view,basename='client_view')
router.register(r'client_update',views.client_update,basename='client_update')
router.register(r'Like_views',views.Like_views,basename='Like_views')
router.register(r'DisLike_views',views.DisLike_views,basename='DisLike_views')
router.register(r'Post_get_by_user',views.Post_get_by_user,basename='Post_get_by_user')
router.register(r'post_content_create',views.post_content_create,basename='post_content_create')
router.register(r'post_view',views.post_view,basename='post_view')##------------------------------------------
router.register(r'Comment_views',views.Comment_views,basename='Comment_views')
router.register(r'Comment_by_post',views.Comment_by_post,basename='Comment_by_post')
router.register(r'Friend_request',views.Friend_request,basename='Friend_request')
router.register(r'friendrequest_update',views.friendrequest_update,basename='friendrequest_update')
router.register(r'friendrequestgetbyFromser',views.friendrequestgetbyFromser,basename='friendrequestgetbyFromser')
router.register(r'friendrequestgetbyTouser',views.friendrequestgetbyTouser,basename='friendrequestgetbyTouser')
router.register(r'friend_List',views.friend_List,basename='friend_List')





router.register(r'state',views.Stat_views,basename='state')
router.register(r'city',views.City_View,basename='city')
#router.register(r'Institute_views',views.Institute_views,basename='Institute')
router.register(r'login_client',views.login_client1,basename='login_client')
router.register(r'technical',views.technical_view,basename='technical')
router.register(r'nontechnical',views.nontechnical_view,basename='nontechnical')
router.register(r'institute_get',views.institute_get,basename='institute_get')
urlpatterns=router.urls
