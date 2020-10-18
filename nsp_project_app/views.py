from django.shortcuts import render

from rest_framework import viewsets
from nsp_project_app import ml
from rest_framework.generics import ListAPIView
import requests
import pandas as pd
#from nsp_project_app.permission import checkuser,IsOwnerOrReadOnlyy

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
#from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from nsp_project_app.models import State,City,post,Like,UnLike,Comment,FriendRequest,User_info,Technical,NonTechnical,Institute,Content,Followers_User
from  django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter,SearchFilter

from nsp_project_app.serializers import State_serializer,City_serializer,ClientSerializer,Institute_serializer,Post_serializer,Post_serializer_get,Like_serializer,UnLike_serializer,Comment_serializer,FriendRequest_serializer,ClientSerializer_update,login_client,technical,non_technical,InstituteSerializer_get,InstituteSerializer_get,Post_serializer_get,Post_Content_serializer,UnLike_serializer,FriendRequest_serializer_update

 #Create your views here.
class Stat_views(viewsets.ViewSet):
    http_method_names =['put','patch','get']

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
        print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)



class client_view(viewsets.ViewSet):

     def create(self,request):

        serializers=ClientSerializer(data=request.data)
        print('-----------------------------------------------------------------------------------------')
        if serializers.is_valid():

            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)



class client_update(viewsets.ViewSet):

    #permission_classes = [.]
    #print('-------------------------------------- 56 view ')
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [checkuser]



    http_method_names =['put','patch','get']



    def partial_update(self, request,pk=None):
        print(request.user,'--------------------------------------------------------------122')
        print('joo')
        try:

            user_related=User.objects.get(username=request.user)
        except:
            return Response('login issue occur')
        print(user_related,'==============================================================================================')
        try:

            user=User_info.objects.get(id=pk)
        except:
            return Response('login issue occur')

        #print(user,'pppppppppppppppppppppppppppp')


        p=request.data
        print(p,'hi')

        user.Institute=request.data.get('Institute',user.Institute)
        #print(user.name,'iiiiiiiiiiiiiiiiiiiiii')
        #user.last_name=request.data.get('last_name',user.last_name)
        #print(user.last_name,'---------------------------------------')
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
            print('=====================================100000000000000000000000000000000001')
            user.NonTechnicalField=NonTechnical.objects.get(id=t_id)

        except:
            print('[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[')
            user.NonTechnicalField=request.data.get(user.NonTechnicalField)
        user.Age=request.data.get('Age',user.Age)
        user.name=request.data.get('name',user.name)

        user.BirthDate=request.data.get('BirthDate',user.BirthDate)
        user.email=request.data.get('email',user.email)





        #print(user_related.driver_email,'---------------------------------------')
        user.save()
        serializer=ClientSerializer_update(user)
        print('============================================================================================')
        return Response(serializer.data)


    def get(self,request,pk=None):
        queryset=User_info.objects.get(id=pk)
        serializer=ClientSerializer_update(queryset)
        print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)


    def list(self,request):
        queryset=User_info.objects.all()
        serializer=ClientSerializer_update(queryset,many=True)
        print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)

















class City_View(viewsets.ViewSet):

    http_method_names =['put','patch','get']

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
        print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)


class Institute_views(viewsets.ViewSet):

    def create(self,request):


        serializers=Institute_serializer(data=request.data)
        print('-----------------------------------------------------------------------------------------')
        if serializers.is_valid():

            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)

class login_client1(viewsets.ViewSet):
    def create(self,request):
        serializers=login_client(data=request.data)
        if serializers.is_valid():

            user=serializers.data['username']
            print('ooooooooooooooooooooooo90')
            o=User.objects.get(username=user)
            login_client(request,o)
            c=User_info.objects.get(username=o)
            print('ooooooooooooooooooooooo91')
            token,created=Token.objects.get_or_create(user=o)
            return Response({"token":token.key,'success':1,"id":c.id},status=200)
        else:
            return Response(serializers.errors)



class technical_view(viewsets.ViewSet):
    def list(self,request):
        queryset=Technical.objects.all()
        serializer=technical(queryset,many=True)
        print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)


class nontechnical_view(viewsets.ViewSet):
    def list(self,request):
        queryset=NonTechnical.objects.all()
        serializer=non_technical(queryset,many=True)
        print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)


class institute_get(viewsets.ViewSet):
    def list(self,request):
        queryset=Institute.objects.all()
        serializer=InstituteSerializer_get(queryset,many=True)
        print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)


'''
class post_content(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        user=request.user
        print(request.auth.key,'--------------------------------1234')
        token=request.auth.key
        print(user,'==============hhhhhhhhhhhhhhhhhhhhhh=qwe')
        c1=User_info.objects.get(username=user)
        serializer=Post_Content_serializer(data=request.data)
        if serializer.is_valid():
            print('-------------------777---------------------------------------------------')
            serializer.save()
            c=Content.objects.latest('id')
            post.objects.create(Post_Content=c,User=c1).save()
            #dada_x=Post_Content_serializer(x)
            #x="12f3"
            #int(x)

            #x = requests.get('http://127.0.0.1:8000/app/Post_get')
            http://127.0.0.1:8000/app/friend_List/
            #print(x,'-------------------------------------------internal')
            p="Token"+str(token)
            print(p,'=====================================12345678')
            response = requests.get(
           http://127.0.0.1:8000/app/Post_get', headers={'Authorization': 'Token 84befe892bd871a19d0793d1dedf9bade182616b})
            print(response,'-----------------------------------------------token')



            return Response(serializer.data)
        else:
            return Response(serializer.errors)



class Post_create(viewsets.ViewSet):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    def create(self,request):
        print('welcome--------------------------------------------------')
        user=request.user
        #print(user,'===============qwe')
        c=User_info.objects.get(username=user)
        print(c,'------------------------------------------------')



        serializers=Post_serializer(data=request.data)
        print('-----------------------------------------------------------------------------------------')
        if serializers.is_valid():
            print(serializers.data['Post_Content']['Image'],'---------------------------------------qwertyuio')
            image=serializers.data['Post_Content']['Image']
            text=serializers.data['Post_Content']['Text']
            content=Content.objects.create(Image=image,Text=text)
            content.save()
            print(content,'================================')
            p_title=serializers.data['Post_Title']
            f=post.objects.create(Post_Title=p_title,Post_Content=content,User=c)
            f.save()
            print(f,'posystststststststststststststsst')




            return Response(serializers.data)
        else:
            return Response(serializers.errors)

'''




class Like_views(viewsets.ViewSet):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def create(self,request):

        serializers=Like_serializer(data=request.data)
        if serializers.is_valid():

            post1=serializers.data['Post']
            print(post,'===========================================')
            try:

                c=post.objects.get(id=post1)
            except:
                return Response("Post not present")
            c.LikeCount=c.LikeCount+1
            c.save()
            print(c,'==========c.==================================')
            user=request.user
            u=User_info.objects.get(username=user)
            print(u,'oooooooooooooooooooooooooooooooooooooooooooooooooo')

            l=Like.objects.create(User=u,Post=c,LikeCount=1)
            l.save()
            return Response({'like':c.LikeCount,'Post':c.id,'like_count':l.LikeCount})
        else:
            return Response(serializers.errors)

class DisLike_views(viewsets.ViewSet):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def create(self,request):

        serializers=UnLike_serializer(data=request.data)
        if serializers.is_valid():

            post1=serializers.data['Post']
            print(post,'===========================================')
            try:

                c=post.objects.get(id=post1)
            except:
                return Response("Post not present")
            c.UnLikeCount=c.UnLikeCount+1
            c.save()
            print(c,'==========c.==================================')
            user=request.user
            u=User_info.objects.get(username=user)
            print(u,'oooooooooooooooooooooooooooooooooooooooooooooooooo')

            l=UnLike.objects.create(User=u,Post=c,UnLikeCount=1)
            l.save()
            return Response({'Unlike':c.UnLikeCount,'Post':c.id,'Unlike_count':l.UnLikeCount})
        else:
            return Response(serializers.errors)






class Comment_views(viewsets.ViewSet):
    def create(self,request):
        serializers=Comment_serializer(data=request.data)
        if (serializers.is_valid()):


            user=request.user
            u=User_info.objects.get(username=user)
            print(u,'oooooooooooooooooooooooooooooooooooooooooooooooooo')

            comment=serializers.data['Post_comment']
            post1=serializers.data['Post']

            try:
                c=post.objects.get(id=post1)
            except:
                return Response("Post not present")
            Comment.objects.create(User=u,Post_comment=comment,Post=c).save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)


class Comment_by_post(viewsets.ViewSet):
    def retrieve(self,request,pk=None):
        print('slug ============',pk)
        queryset=Comment.objects.filter(Post=pk)
        serializer=Comment_serializer_notification(queryset,many=True)
        print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)










class Post_get_by_user(viewsets.ViewSet):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def list(self,request):
        user=request.user
        c=User_info.objects.get(username=user)

        queryset=post.objects.filter(User=c)
        serializer=Post_serializer_get(queryset,many=True)
        print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)

class post_view(viewsets.ViewSet):
    def list(self,request):
        queryset=post.objects.all().order_by('-id')
        user=request.user
        print(user,'userrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        u=User_info.objects.get(username=user)
        print(u.id,'iddddddddddddddddddddddddddddddddddddddddddd')
        l=[]
        d=[]
        userinfo=[]
        userinfo.append({"username":u.id,"name":u.name,"Institute":u.Institute,"TechnicalField":u.TechnicalField.TechnicalName,"NonTechnicalField":u.NonTechnicalField.NonTechnicalName,"city_Name":u.city_Name.CityName,"CreatedDate_user":u.CreatedDate,"UpdateDate_user":u.UpdateDate})
        image=[]
        for i in queryset:


            print(i.User.email,'---h-----',i.Post_Content.Image)
            if(i.Post_Content.Image):
                print('---------image')


                d.append({"Id":i.Post_Content.id,"username": i.User.id,"CreatedDate":i.CreatedDate,"UpdateDate":i.UpdateDate,"LikeCount":i.LikeCount,"UnLikeCount":i.UnLikeCount,"Institute_user_post":i.User.Institute,"TechnicalField":i.User.TechnicalField.TechnicalName,"NonTechnicalField":i.User.NonTechnicalField.NonTechnicalName,"city_Name":i.User.city_Name.CityName,"post_title":i.Post_Content.Post_Title,"Text":i.Post_Content.Text,"Image":i.Post_Content.Image,"CreatedDate_user":u.CreatedDate,"UpdateDate_user":u.UpdateDate})
            else:
                print('---------notimage')

                image.append({"Id":i.Post_Content.id,"username": i.User.id,"CreatedDate":i.CreatedDate,"UpdateDate":i.UpdateDate,"LikeCount":i.LikeCount,"UnLikeCount":i.UnLikeCount,"Institute_user_post":i.User.Institute,"TechnicalField":i.User.TechnicalField.TechnicalName,"NonTechnicalField":i.User.NonTechnicalField.NonTechnicalName,"city_Name":i.User.city_Name.CityName,"post_title":i.Post_Content.Post_Title,"Text":i.Post_Content.Text,"CreatedDate_user":i.User.CreatedDate,"UpdateDate_user":i.User.UpdateDate})








        #print(queryset,'----------------ram----------------------------')
        print(ml.add(d,image,userinfo))
        print("------------ Id below------------------")
        print(ml.add(d,image,userinfo))
        #print(ml.add())

        response = requests.get(
           'http://127.0.0.1:8000/app/friend_List/', headers={'Authorization': "Token 84befe892bd871a19d0793d1dedf9bade182616b"})
    #    print(ml.add(d,image,userinfo))
        print("ohhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh____2_____Yeeeaaaaaaahhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

        print(response,'fuckkkkkkkkkkkkkkkkk')


        serializer=Post_serializer_get(queryset,many=True)
        #print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)
class post_content_create(viewsets.ViewSet):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def create(self,request):
        user=request.user
        print(user,'==============hhhhhhhhhhhhhhhhhhhhhh=qwe')
        c1=User_info.objects.get(username=user)
        serializer=Post_Content_serializer(data=request.data)
        if serializer.is_valid():
            print('-------------------777---------------------------------------------------')
            serializer.save()
            c=Content.objects.latest('id')
            post.objects.create(Post_Content=c,User=c1).save()


            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class Friend_request(viewsets.ViewSet):
    def create(self,request):
        serializers=FriendRequest_serializer(data=request.data)
        if (serializers.is_valid()):

            user=request.user
            print(user,'===================================================================123')
            try:

                u=User_info.objects.get(username=user)
                print(u,'===================================================================124')

            except:


                return Response("User not present")




            to=serializers.data['ToUser']
            try:

                c=User_info.objects.get(username=to)
                print(c,'===================================================================124')

            except:
                return Response("User not present")

            FriendRequest.objects.create(FromUser=u,ToUser=c).save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
    def list(self,request):
        user=request.user
        u=User_info.objects.get(username=user)
        queryset=FriendRequest.objects.filter(ToUser=u).filter(Status=0)
        serializer=FriendRequest_serializer(queryset,many=True)
        print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)






class friendrequestgetbyTouser(viewsets.ViewSet):
    '''serializer_class = FriendRequest_serializer
    queryset = FriendRequest.objects.all()
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filter_fields=('ToUser','FromUser','id')'''
    def list(self,request):
        user=request.user
        u=User_info.objects.get(username=user)
        queryset=FriendRequest.objects.filter(ToUser=u).filter(Status=0)
        serializer=FriendRequest_serializer(queryset,many=True)
        print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)



class friendrequestgetbyFromser(viewsets.ViewSet):
    def list(self,request):
        user=request.user
        u=User_info.objects.get(username=user)
        queryset=FriendRequest.objects.filter(FromUser=u).filter(Status=0)
        serializer=FriendRequest_serializer(queryset,many=True)
        print(serializer.data,']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        return Response(serializer.data)

class friend_List(viewsets.ViewSet):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def list(self,request):
        user=request.user
        u=User_info.objects.get(username=user)
        queryset=FriendRequest.objects.filter(ToUser=u).filter(Status=1)
        serializer=FriendRequest_serializer(queryset,many=True)
        d=Followers_User.objects.all()
        z=[]
        for i in d:
            z.append({"user":i.User.id,"Follower":i.Followers.id})
            print(i,'-------hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhggg-----')
        print(z,'----------hhhhgggggggggggggggggggggggggggggggggggggggddh')
        df=pd.DataFrame(z)
        print(df,'----------')
        df.to_csv("C:/Users/Ankesh/Desktop/followers_data.csv")







class friendrequest_update(viewsets.ViewSet):
    def partial_update(self,request,pk=None):
        try:

            c=FriendRequest.objects.get(id=pk)
        except:
            return Response('not present')
        s=request.data.get('Status')
        print(type(s),'=================================================================')
        if(s=='1'):
            print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            c.Status=1
            c.save()
            serializers=FriendRequest_serializer_update(c)
            return Response(serializers.data)
        else:
            FriendRequest.objects.get(id=pk).delete()
            return Response("ok")
