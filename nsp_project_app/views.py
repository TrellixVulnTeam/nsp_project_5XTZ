from django.shortcuts import render
#from rest_framework import viewsets
from nsp_project_app import ml
from nsp_project_app import ml_friend
from rest_framework.generics import ListAPIView
import requests
import pandas as pd
from rest_framework import viewsets
from nsp_project_app.permission import checkuser,IsOwnerOrReadOnlyy
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from nsp_project_app.models import State,City,post,Like,UnLike,Comment,FriendRequest,User_info,Technical,NonTechnical,Content,Notification,Followers_User
from  django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter,SearchFilter

from nsp_project_app.serializers import State_serializer,City_serializer,ClientSerializer,Post_serializer,Post_serializer_get,Like_serializer,UnLike_serializer,Comment_serializer,FriendRequest_serializer,ClientSerializer_update,login_client,technical,non_technical,Post_serializer_get,Post_Content_serializer,UnLike_serializer,FriendRequest_serializer_update,notification_serializer,FriendRequest_serializer_create,Comment_serializer_notification,follower_serializer,friend_reccomendation_serializer

 #Create your views here.
class Stat_views(viewsets.ViewSet):

    def create(self,request):

        serializers=State_serializer(data=request.data)
        if serializers.is_valid():

            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
    def list(self,request):
        queryset=State.objects.all()
        serializer=State_serializer(queryset,many=True)
        return Response(serializer.data)



class client_view(viewsets.ViewSet):



    def create(self,request):


        serializers=ClientSerializer(data=request.data)
        if serializers.is_valid():

            serializers.save()
            return Response({"data":serializers.data,"token":1234455,"status":200})
        else:
            return Response(serializers.errors)

class client_get(viewsets.ViewSet):
    def list(self,request):
        queryset=User_info.objects.all()
        serializer=ClientSerializer_update(queryset,many=True)
        return Response(serializer.data)





class client_update(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



    http_method_names =['put','patch','get']



    def partial_update(self, request,pk=None):
        try:

            user_related=User.objects.get(username=request.user)
        except:
            return Response('login issue occur')
        try:

            user=User_info.objects.get(id=pk)
        except:
            return Response('login issue occur')



        p=request.data

        user.Institute=request.data.get('Institute',user.Institute)
        user.img=request.data.get("img",user.img)

        try:
            t_id=request.data.get('TechnicalField',user.TechnicalField)


            user.TechnicalField=Technical.objects.get(id=t_id)

        except:
            user.TechnicalField=request.data.get('TechnicalField',user.TechnicalField)
        try:
            s_id=request.data.get('State_Name',user.State_Name)
            user.State_Name=State.objects.get(id=s_id)

        except:
            user.State_Name=request.data.get('State_Name',user.State_Name)
        try:
            c_id=request.data.get('city_Name',user.city_Name)
            user.city_Name=City.objects.get(id=s_id)

        except:
            user.city_Name=request.data.get('city_Name',user.city_Name)
        try:
            t_id=request.data.get('NonTechnicalField',user.NonTechnicalField)
            user.NonTechnicalField=NonTechnical.objects.get(id=t_id)

        except:
            user.NonTechnicalField=request.data.get(user.NonTechnicalField)
        user.Age=request.data.get('Age',user.Age)
        user.name=request.data.get('name',user.name)

        user.BirthDate=request.data.get('BirthDate',user.BirthDate)
        user.email=request.data.get('email',user.email)
        user.save()
        serializer=ClientSerializer_update(user)
        return Response(serializer.data)


    def get(self,request,pk=None):
        try:

            queryset=User_info.objects.get(id=pk)
        except:
            return Response("User not present")
        serializer=ClientSerializer_update(queryset)
        return Response(serializer.data)


class City_View(viewsets.ViewSet):
    def create(self,request):

        serializers=City_serializer(data=request.data)
        if serializers.is_valid():

            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
    def list(self,request):
        queryset=City.objects.all()
        serializer=City_serializer(queryset,many=True)
        return Response(serializer.data)




class login_client1(viewsets.ViewSet):
    def create(self,request):
        serializers=login_client(data=request.data)
        if serializers.is_valid():

            user=serializers.data['username']
            o=User.objects.get(username=user)
            login_client(request,o)
            c=User_info.objects.get(username=o)
            token,created=Token.objects.get_or_create(user=o)
            return Response({"token":token.key,'success':1,"id":c.id},status=200)
        else:
            return Response(serializers.errors)



class technical_view(viewsets.ViewSet):
    def list(self,request):
        queryset=Technical.objects.all()
        serializer=technical(queryset,many=True)
        return Response(serializer.data)

    def create(self,request):

        serializers=technical(data=request.data)
        if serializers.is_valid():

            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)


class nontechnical_view(viewsets.ViewSet):
    def list(self,request):
        queryset=NonTechnical.objects.all()
        serializer=non_technical(queryset,many=True)
        return Response(serializer.data)
    def create(self,request):


        serializers=non_technical(data=request.data)
        if serializers.is_valid():

            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)

class Like_views(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):

        serializers=Like_serializer(data=request.data)
        if serializers.is_valid():

            post1=serializers.data['Post']
            user=request.user
            try:



                u=User_info.objects.get(username=user)
            except:


                return Response("user not present")
            try:

                c=post.objects.get(id=post1)

                UnLike.objects.filter(Post=c).get(User=u).delete()
                c.UnLikeCount=c.UnLikeCount-1
            except:

                pass
            try:

                s=Like.objects.filter(Post=c).get(User=u)


                if(s):
                    c.LikeCount=c.LikeCount-1
                    c.save()
                    Like.objects.filter(Post=c).get(User=u).delete()
                    return Response({'like':c.LikeCount,'Post':c.id,'like_count':0,"status":200})




            except:
                c.LikeCount=c.LikeCount+1
                c.save()


                l=Like.objects.create(User=u,Post=c,LikeCount=1)
                l.save()
                Notification.objects.create(Like=l,total=1,user=c.User).save()
                return Response({'like':c.LikeCount,'Post':c.id,'like_count':l.LikeCount,"status":200})
        else:
            return Response(serializers.errors)

class DisLike_views(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):

        serializers=UnLike_serializer(data=request.data)
        if serializers.is_valid():

            post1=serializers.data['Post']
            c=post.objects.get(id=post1)

            user=request.user
            try:

                u=User_info.objects.get(username=user)
            except:

                return Response("user not present")

            try:
                c=post.objects.get(id=post1)

                Like.objects.filter(Post=c).get(User=u).delete()

                c.LikeCount=c.LikeCount-1
            except:
                pass



            try:


                s=UnLike.objects.filter(Post=c).get(User=u)






                if(s):

                    c.UnLikeCount=c.UnLikeCount-1
                    c.save()
                    UnLike.objects.filter(Post=c).get(User=u).delete()
                    return Response({'Unlike':c.UnLikeCount,'Post':c.id,'Unlike_count':0,"status":200})

            except:

                c.UnLikeCount=c.UnLikeCount+1
                c.save()


                l=UnLike.objects.create(User=u,Post=c,UnLikeCount=1)
                l.save()
                Notification.objects.create(UnLike=l,total=1,user=c.User).save()

                return Response({'Unlike':c.UnLikeCount,'Post':c.id,'Unlike_count':l.UnLikeCount,"status":200})
        else:
            return Response(serializers.errors)
    def list(self,request):
        queryset=UnLike.objects.all()
        serializer=UnLike_serializer(queryset,many=True)
        return Response(serializer.data)







class Comment_views(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        serializers=Comment_serializer(data=request.data)

        if (serializers.is_valid()):


            user=request.user
            try:

                u=User_info.objects.get(username=user)
            except:

                return Response("user not present")


            comment=serializers.data['Post_comment']
            post1=serializers.data['Post']

            try:
                c=post.objects.get(id=post1)
            except:
                return Response("Post not present")
            a=Comment.objects.create(User=u,Post_comment=comment,Post=c)
            a.save()
            Notification.objects.create(comment=a,total=1,user=c.User).save()

            return Response({"Status":200})
        else:
            return Response(serializers.errors)


class Comment_by_post(viewsets.ViewSet):
    def retrieve(self,request,pk=None):
        try:

            queryset=Comment.objects.filter(Post=pk)
        except:
            return Response("post not present")
        serializer=Comment_serializer_notification(queryset,many=True)
        return Response(serializer.data)













class Post_get_by_user(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        user=request.user
        try:

            c=User_info.objects.get(username=user)
        except:

            return Response("user not present")


        queryset=post.objects.filter(User=c)
        serializer=Post_serializer_get(queryset,many=True)
        return Response(serializer.data)
    def retrieve(self,request,pk=None):
        try:

            c=User_info.objects.get(id=pk)
        except:

            return Response("user not present")


        queryset=post.objects.filter(User=c)
        serializer=Post_serializer_get(queryset,many=True)
        return Response(serializer.data)
class post_get_by_title(viewsets.ViewSet):
    def retrieve(self,request,pk=None):

        queryset=post.objects.filter(Title=pk)
        serializer=Post_serializer_get(queryset,many=True)
        return Response(serializer.data)














class post_view(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        queryset=post.objects.all()
        p=Like.objects.all()
        l1=[]
        d1=[]
        for i in p:
            if(i.User.id==1):

                l1.append(i.Post.id)

        user=request.user

        try:

            u=User_info.objects.get(username=user)
        except:
            return Response("user not present")



        serializer=Post_serializer_get(queryset,many=True)
        return Response(serializer.data)
class post_content_create(viewsets.ViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        user=request.user
        try:

            c1=User_info.objects.get(username=user)
        except:
            return Response("user not present")

        serializer=Post_Content_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            c=Content.objects.latest('id')
            post.objects.create(Post_Content=c,User=c1,Title=c.Post_Title).save()


            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class Friend_request(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self,request):
        serializers=FriendRequest_serializer_create(data=request.data)
        if (serializers.is_valid()):

            user=request.user

            try:

                u=User_info.objects.get(username=user)

            except:


                return Response("user not present")



            to=serializers.data['ToUser']
            try:

                c=User_info.objects.get(id=to)

            except:
                return Response("user not present")
            try:


                a=FriendRequest.objects.create(FromUser=u,ToUser=c)
            except:
                return Response("User not matched")
            a.save()
            Notification.objects.create(friend=a,total=1,user=c).save()

            return Response(serializers.data)
        else:
            return Response(serializers.errors)
    def list(self,request):
        user=request.user
        try:

            u=User_info.objects.get(username=user)
        except:
            return Response("user not present")
        queryset=FriendRequest.objects.all()
        serializer=FriendRequest_serializer_create(queryset,many=True)
        return Response(serializer.data)












class friendrequestgetbyTouser(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        user=request.user
        try:

            u=User_info.objects.get(username=user)

        except:
            return Response({"status":404})
        queryset=FriendRequest.objects.filter(ToUser=u).filter(Status=0)
        serializer=FriendRequest_serializer(queryset,many=True)
        return Response(serializer.data)



class friendrequestgetbyFromuser(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        user=request.user
        try:

            u=User_info.objects.get(username=user)

        except:
            return Response("user not present")



        queryset=FriendRequest.objects.filter(FromUser=u).filter(Status=0)
        serializer=FriendRequest_serializer(queryset,many=True)
        return Response(serializer.data)
    def partial_update(self,request,pk=None):
        try:


            FriendRequest.objects.get(id=pk).delete()
            return Response({"status":200})

        except:
            return Response({"status":500})





class friend_List(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        user=request.user
        try:

            u=User_info.objects.get(username=user)
        except:
            return Response("user not present")
        queryset=FriendRequest.objects.filter(ToUser=u).filter(Status=1)
        queryset1=FriendRequest.objects.filter(FromUser=u).filter(Status=1)
        s=queryset.union(queryset1)
        serializer=FriendRequest_serializer(s,many=True)
        return Response(serializer.data)










class friendrequest_update(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def partial_update(self,request,pk=None):
        try:


            c=FriendRequest.objects.get(id=pk)
        except:
            return Response('Friend not present')
        s=request.data.get('Status')
        if(s==1):
            c.Status=1
            c.save()
            serializers=FriendRequest_serializer_update(c)
            return Response({"status":"200"})


        else:
            FriendRequest.objects.get(id=pk).delete()
            return Response({"status":"200"})


class like_check(viewsets.ViewSet):
    def create(self,request):

        serializers=Like_serializer(data=request.data)
        if serializers.is_valid():
            po=serializers.data['Post']
            user=request.user
            u=User_info.objects.get(username=user)
            p=Like.objects.filter(Post=po,User=u)
            if(p):

                return Response("ok")
            else:

                return Response("no")
        else:
            return Response(serializers.errors)
    def list(self,request):
        queryset=Like.objects.all()
        serializer=Like_serializer(queryset,many=True)
        return Response(serializer.data)






class Search_user(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ClientSerializer_update
    queryset = User_info.objects.all()
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filter_fields=('name','id')
    ordering_fields=('CreatedDate')



class Notification_by_user(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','put','patch']
    def list(self,request):
        user=request.user
        try:

            u=User_info.objects.get(username=user)
        except:
            return Response("User not present")
        queryset=Notification.objects.filter(user=u).filter(status=0)
        serializer=notification_serializer(queryset,many=True)
        return Response(serializer.data)
    def partial_update(self,request,pk=None):
        user=request.user
        try:

            u=User_info.objects.get(username=user)
        except:

            return Response("User not present")


        queryset=Notification.objects.filter(user=u).filter(status=0)
        for i in queryset:
            i.status=1
            i.save()
        serializer=notification_serializer(queryset)
        return Response({"status":200})





class friend_check_serializer(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        serializer=FriendRequest_serializer_create(data=request.data)
        user=request.user





        if(serializer.is_valid()):


            try:

                u=User_info.objects.get(username=user)
            except:

                return Response("error")


            try:
                c=serializer.data['FromUser']

                user2=User.objects.get(id=c)

                u2=User_info.objects.get(username=user2)
            except:

                return Response("error")
            try:



                f=FriendRequest.objects.filter(FromUser=u2).filter(ToUser=u)
                return Response({"Status":1})
            except:
                try:

                    f2=FriendRequest.objects.filter(FromUser=u).filter(ToUser=u2)
                    return Response({"Status":2})
                except:

                    return Response({"Status":0})
        else:
            return Response(serializer.errors)





class follower_view(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        user=request.user
        try:

            u=User_info.objects.get(username=user)
        except:

            return Response("Invalid username")

        p=request.data.get('Followers')
        try:

            d=User.objects.get(id=p)
            f=User_info.objects.get(username=d)
            Followers_User.objects.create(User=f,Followers=u).save()
            return Response({"status":200})

        except:
            return Response("Invalid username")



    def list(self,request):
        queryset=Followers_User.objects.all()
        serializer=follower_serializer(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self,request,pk=None):
        user=request.user
        try:


            u=User_info.objects.get(username=user)

            c=User.objects.get(id=pk)
            d=User_info.objects.get(username=c)
            g=Followers_User.objects.filter(Followers=u).filter(User=d)
            return Response({"status":200})

        except:
            return Response("Invalid username")





class friend_reccomendation(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        serializer=follower_serializer()
        if 1:
            u=request.user
            print(u,'============')

            try:


                x=User.objects.get(username=u)


                u=User_info.objects.get(username=x)




            except:

                return Response("user not present")

            d=Followers_User.objects.all()
            z=[]
            for i in d:
                z.append({"user":i.User.id,"Follower":i.Followers.id})
            df=pd.DataFrame(z)
            print(df)
            try:

                c=ml_friend.FriendGraph(df)
            except:
                return Response("Something Wrong")

            g=[]
            data=[]
            print(c.recommend_friend(u.id),'-------jj----------------')















            try:
                for i in c.recommend_friend(u.id):

                    g.append(i)
                    print(g,'=========================7878')

                if(len(g)==0):
                    return Response("0")
                else:
                    f=User_info.objects.all()
                    for u in f:
                        if(u.id in g and u.id!=x.id ):
                            print('=========================',u.img,'-----------')
                            try:



                                data.append({"image":u.img.url,"id":u.id,"name":u.name})
                            except:


                                data.append({"image":0,"id":u.id,"name":u.name})


                if(len(data)==0):
                    return Response("0")







                return Response(data)
            except:

                return Response("0")





        else:
            return Response(serializer.errors)


class post_reccomendation(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):

        user=request.user
        print(user,'-------------------')
        u=User_info.objects.get(username=user)


        try:

            u=User_info.objects.get(username=user)
        except:
            return Response("user not present")



        l=[]
        d=[]
        userinfo=[]
        userinfo.append({"username":u.id,"name":u.name,"Institute":u.Institute,"TechnicalField":u.TechnicalField.TechnicalName,"NonTechnicalField":u.NonTechnicalField.NonTechnicalName,"city_Name":u.city_Name.CityName,"CreatedDate_user":u.CreatedDate,"UpdateDate_user":u.UpdateDate})
        image=[]
        queryset=post.objects.all()



        try:






            for i in queryset:





                image.append({"Id":i.Post_Content.id,"username": i.User.id,"CreatedDate":i.CreatedDate,"UpdateDate":i.UpdateDate,"LikeCount":i.LikeCount,"UnLikeCount":i.UnLikeCount,"Institute_user_post":i.User.Institute,"TechnicalField":i.User.TechnicalField.TechnicalName,"NonTechnicalField":i.User.NonTechnicalField.NonTechnicalName,"city_Name":i.User.city_Name.CityName,"post_title":i.Post_Content.Post_Title,"Text":i.Post_Content.Text,"CreatedDate_user":i.User.CreatedDate,"UpdateDate_user":i.User.UpdateDate})
            h=[]
            for i in ml.add(image,userinfo):
                for j in i:

                    h.append(j)
            for g in h:
                for i in queryset:
                    if(i.Post_Content.id==g):
                            if(i.Post_Content.Image and i.User.img):

                                d.append({"id":i.id,"LikeCount":i.LikeCount,"UnLikeCount":i.UnLikeCount,"content":{
                                    "id":i.Post_Content.id,"Post_Title":i.Post_Content.Post_Title,"Image":i.Post_Content.Image.url,"Text"
                                    :i.Post_Content.Text
                                },


                                          "user":{
                                              "id":i.User.id,"email":i.User.email,"name":i.User.name,"img":i.User.img.url
                                          }

                                          })
                            elif(i.Post_Content.Image):

                                d.append({"id":i.id,"LikeCount":i.LikeCount,"UnLikeCount":i.UnLikeCount,"content":{
                                    "id":i.Post_Content.id,"Post_Title":i.Post_Content.Post_Title,"Image":i.Post_Content.Image.url,"Text"
                                    :i.Post_Content.Text
                                },


                                          "user":{
                                              "id":i.User.id,"email":i.User.email,"name":i.User.name,"img":0
                                          }

                                          })
                            elif(i.User.img):
                                d.append({"id":i.id,"LikeCount":i.LikeCount,"UnLikeCount":i.UnLikeCount,"content":{
                                    "id":i.Post_Content.id,"Post_Title":i.Post_Content.Post_Title,"Image":0,"Text"
                                    :i.Post_Content.Text
                                },


                                          "user":{
                                              "id":i.User.id,"email":i.User.email,"name":i.User.name,"img":i.User.img.url
                                          }

                                          })
                            else:
                                d.append({"id":i.id,"LikeCount":i.LikeCount,"UnLikeCount":i.UnLikeCount,"content":{
                                    "id":i.Post_Content.id,"Post_Title":i.Post_Content.Post_Title,"Image":0,"Text"
                                    :i.Post_Content.Text
                                },


                                          "user":{
                                              "id":i.User.id,"email":i.User.email,"name":i.User.name,"img":0
                                          }

                                          })
            return Response(d)
        except:

            return Response("user post required")
