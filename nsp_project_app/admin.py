from django.contrib import admin

# Register your models here.
from .models import post
from .models import State
from .models import Technical
from .models import NonTechnical
from .models import City
from .models import Institute
from .models import User_info
from .models import Like
from .models import UnLike
from .models import Comment
from .models import FriendRequest
from .models import Followers_User
from .models import Followig_User
from .models import Content
'''
'''
# Register your models here.
admin.site.register(Content)
admin.site.register(post)
admin.site.register(State)
admin.site.register(Technical)
admin.site.register(NonTechnical)
admin.site.register(City)
admin.site.register(Institute)
admin.site.register(User_info)
admin.site.register(Like)
admin.site.register(UnLike)
admin.site.register(Comment)
admin.site.register(FriendRequest)
admin.site.register(Followers_User)
admin.site.register(Followig_User)
