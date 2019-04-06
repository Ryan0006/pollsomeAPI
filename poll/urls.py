from django.urls import path
from . import views

app_name = 'poll'

urlpatterns = [
    path('vote/', views.PollVotes.as_view(), name='votes'),
    path('poll/<int:poll_id>/<str:user_id>',
         views.PollDetail.as_view(), name='poll'),
    path('poll/', views.PollEdit.as_view(), name='poll_edit'),
    path('allpolls/<str:user_id>', views.AllPolls.as_view(), name='all_polls'),
    path('mypolls/<int:user_id>', views.MyPolls.as_view(), name='my_polls'),
    path('comment/', views.CommentDetail.as_view(), name='comment'),
    path('like/', views.LikeDetail.as_view(), name='like'),
    path('pollcomments/<int:pollId>',
         views.PollComments.as_view(), name='poll_comments'),
]
