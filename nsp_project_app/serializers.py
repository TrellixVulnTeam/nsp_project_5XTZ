#_author__ = 'PRIYANSH KHANDELWAL'
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from rest_framework import exceptions
from nsp_project_app.models import State,City,User_info,post,Content,Like,UnLike,Comment,FriendRequest,Technical,NonTechnical,Notification,Followers_User








class State_serializer(serializers.ModelSerializer):
    class Meta:
        model=State
        fields='__all__'
class City_serializer(serializers.ModelSerializer):

    class Meta:
        model=City
        fields='__all__'





class technical_serializer(serializers.ModelSerializer):

    class Meta:
        model=Technical
        fields='__all__'



class nontechnical_serializer(serializers.ModelSerializer):

    class Meta:
        model=NonTechnical
        fields='__all__'







class UserSerializer(serializers.ModelSerializer):
    #id = serializers.CharField(source='pk', read_only=True)
    class Meta:
        model = User
        fields = ['username','id']



class ClientSerializer(serializers.ModelSerializer):
    username = UserSerializer()

    password=serializers.CharField(write_only=True,max_length=10)
    confirm_password = serializers.CharField(write_only=True,max_length=10)



    class Meta:

        model = User_info
        fields = ['Institute','username','email','TechnicalField','NonTechnicalField','password','confirm_password','BirthDate','city_Name','name','img']


    def validate(self, data):
        user_password = data.get('password')




        if user_password != data.pop('confirm_password'):

            raise serializers.ValidationError("Passwords do not match")
        else:




            return data



    def create(self, validated_data):

        user_data=validated_data.pop('username')
        password=validated_data.pop("password")
        user=User.objects.create(**user_data)
        user.set_password(password)
        user.save()


        client = User_info.objects.create(username=user, **validated_data)
        return client
    def to_representation(self, instance):

        response=super().to_representation(instance)
        #response['user']=UserSerializer(instance.username).data
        response['Technical']=technical_serializer(instance.TechnicalField).data
        response['NonTechnical']=nontechnical_serializer(instance.NonTechnicalField).data
        response['City']=City_serializer(instance.city_Name).data
        return response

class Post_Content_serializer(serializers.ModelSerializer):
    class Meta:
        model=Content
        fields='__all__'



class Post_serializer(serializers.ModelSerializer):

    class Meta:
        model=post
        fields=['User']



















class FriendRequest_serializer_create(serializers.ModelSerializer):

    class Meta:


            model=FriendRequest
            fields='__all__'


class FriendRequest_serializer_update(serializers.ModelSerializer):

    class Meta:


            model=FriendRequest
            fields=['Status']


class ClientSerializer_update(serializers.ModelSerializer):



    class Meta:



        model=User_info
        fields = ['Institute','email','BirthDate','name','Age','img','id']
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['state']=State_serializer(instance.State_Name).data
        #response['city_Name']=City_serializer(instance.city_Name).data
        response['TechnicalField']=technical_serializer(instance.TechnicalField).data
        response['NonTechnicalField']=nontechnical_serializer(instance.NonTechnicalField).data
        response['city_Name']=City_serializer(instance.city_Name).data
        response['username']=UserSerializer(instance.username).data


        return response




class FriendRequest_serializer(serializers.ModelSerializer):

    class Meta:


            model=FriendRequest
            fields='__all__'
    def to_representation(self, instance):
        response=super().to_representation(instance)
        #response['user']=UserSerializer(instance.username).data
        response['To_User']=ClientSerializer_update(instance.ToUser).data
        response['From_User']=ClientSerializer_update(instance.FromUser).data
        return response




class login_client(serializers.Serializer):
    username=serializers.CharField(max_length=10)
    password=serializers.CharField(max_length=10)
    def validate(self, data):
        username=data.get("username")
        password=data.get("password")
        if username and password:
            user=authenticate(username=username,password=password)
            if user:

                if user.is_active:

                    data['user']=user
                else:
                       msg="Account is deactivated"
                       raise exceptions.ValidationError(msg)

            else:

                msg="password or username not matched"
                raise exceptions.ValidationError(msg)

        else:
            msg="Must provide username and password"
            raise exceptions.ValidationError(msg)
        return data





class technical(serializers.ModelSerializer):
    class Meta:
        model=Technical
        fields='__all__'







class non_technical(serializers.ModelSerializer):

    class Meta:
        model=NonTechnical
        fields='__all__'




class Post_serializer_get(serializers.ModelSerializer):
    class Meta:
        model=post
        fields='__all__'
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['content']=Post_Content_serializer(instance.Post_Content).data
        response['user']=ClientSerializer_update(instance.User).data


        return response


class Like_serializer_notification(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields=['User','Post','LikeCount']

    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['user']=ClientSerializer_update(instance.User).data
        #response['UnLike']=ClientSerializer_update(instance.User).data






        return response




class Like_serializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields=['User','Post','LikeCount']





class UnLike_serializer_notification(serializers.ModelSerializer):
    class Meta:
        model=UnLike
        fields='__all__'
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['user']=ClientSerializer_update(instance.User).data
        #response['UnLike']=ClientSerializer_update(instance.User).data






        return response




class UnLike_serializer(serializers.ModelSerializer):
    class Meta:
        model=UnLike
        fields='__all__'










class Comment_serializer_notification(serializers.ModelSerializer):
        class Meta:

            model=Comment
            fields='__all__'
        def to_representation(self, instance):

            response=super().to_representation(instance)
            response['user']=ClientSerializer_update(instance.User).data
            #response['UnLike']=ClientSerializer_update(instance.User).data






            return response
class Comment_serializer(serializers.ModelSerializer):
        class Meta:

            model=Comment
            fields='__all__'






class notification_serializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields='__all__'

    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['Like']=Like_serializer_notification(instance.Like).data
        response['user']=ClientSerializer_update(instance.user).data
        response['UnLike']=UnLike_serializer_notification(instance.UnLike).data
        response['comment']=Comment_serializer_notification(instance.comment).data
        response['friend']=FriendRequest_serializer(instance.friend).data


        return response
        #response['UnLike']=ClientSerializer_update(instance.User).data

class follower_serializer(serializers.ModelSerializer):
    class Meta:

        model=Followers_User
        fields='__all__'





class friend_reccomendation_serializer(serializers.Serializer):
    User=serializers.CharField(max_length=10)
