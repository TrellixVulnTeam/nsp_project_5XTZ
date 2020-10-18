#_author__ = 'PRIYANSH KHANDELWAL'
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from rest_framework import exceptions
from nsp_project_app.models import State,City,User_info,Institute,post,Content,Like,UnLike,Comment,FriendRequest,Technical,NonTechnical








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
        fields = ['username']



class ClientSerializer(serializers.ModelSerializer):
    username = UserSerializer()

    password=serializers.CharField(write_only=True,max_length=10)
    confirm_password = serializers.CharField(write_only=True,max_length=10)



    class Meta:

        model = User_info
        fields = ['Institute','username','email','TechnicalField','NonTechnicalField','password','confirm_password','BirthDate','city_Name']


    def validate(self, data):
        print(data,'-----------------------------------------')
        user_password = data.get('password')
        print(user_password,'===================')




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


        print('===========',validated_data,'[[=================================================99999999999999999999999999999999999999999999')
        client = User_info.objects.create(username=user, **validated_data)
        print(client,'============================================================1000000')
        return client
    def to_representation(self, instance):

        response=super().to_representation(instance)
        #response['user']=UserSerializer(instance.username).data
        response['Technical']=technical_serializer(instance.TechnicalField).data
        response['NonTechnical']=nontechnical_serializer(instance.NonTechnicalField).data
        response['City']=City_serializer(instance.city_Name).data






        return response







class Institute_serializer(serializers.ModelSerializer):
    username = UserSerializer()

    password=serializers.CharField(write_only=True,max_length=10)
    confirm_password = serializers.CharField(write_only=True,max_length=10)



    class Meta:

        model = Institute
        fields = ['InstituteAddress','username','email','InstitutePhoneNo','State_Name','city_Name','password','confirm_password']


    def validate(self, data):
        print(data,'-----------------------------------------')
        user_password = data.get('password')
        print(user_password,'===================')




        if user_password != data.pop('confirm_password'):

            raise serializers.ValidationError("Passwords do not match")
        else:

            if(len(str(data['InstitutePhoneNo']))!=10):

                raise serializers.ValidationError("No not correct")
            else:
                return data



    def create(self, validated_data):

        user_data=validated_data.pop('username')
        password=validated_data.pop("password")
        user=User.objects.create(**user_data)
        user.set_password(password)
        user.save()


        print('===========',validated_data,'[[=================================================99999999999999999999999999999999999999999999')
        client = Institute.objects.create(username=user, **validated_data)
        print(client,'============================================================1000000')
        return client


class Post_Content_serializer(serializers.ModelSerializer):
    class Meta:
        model=Content
        fields='__all__'



class Post_serializer(serializers.ModelSerializer):

    class Meta:
        model=post
        fields=['User']











class Comment_serializer(serializers.ModelSerializer):
        class Meta:

            model=Comment
            fields='__all__'


class FriendRequest_serializer(serializers.ModelSerializer):

    class Meta:


            model=FriendRequest
            fields='__all__'
    def to_representation(self, instance):
        response=super().to_representation(instance)
        #response['user']=UserSerializer(instance.username).data
        response['To_User']=ClientSerializer(instance.ToUser).data
        response['From_User']=ClientSerializer(instance.FromUser).data
        return response














class FriendRequest_serializer_update(serializers.ModelSerializer):

    class Meta:


            model=FriendRequest
            fields=['Status']


class ClientSerializer_update(serializers.ModelSerializer):



    class Meta:



        model=User_info
        fields = ['Institute','email','BirthDate','name','Age']
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['state']=State_serializer(instance.State_Name).data
        #response['city_Name']=City_serializer(instance.city_Name).data
        response['TechnicalField']=technical_serializer(instance.TechnicalField).data
        response['NonTechnicalField']=nontechnical_serializer(instance.NonTechnicalField).data
        response['city_Name']=City_serializer(instance.city_Name).data
        response['username']=UserSerializer(instance.username).data


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
        print('ppppppppppp77')
        return data





class technical(serializers.ModelSerializer):
    class Meta:
        model=Technical
        fields='__all__'







class non_technical(serializers.ModelSerializer):

    class Meta:
        model=NonTechnical
        fields='__all__'











class InstituteSerializer_get(serializers.ModelSerializer):

    class Meta:

        model=Institute
        fields='__all__'
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['state']=State_serializer(instance.State_Name).data
        response['city_Name']=City_serializer(instance.city_Name).data




        response['username']=UserSerializer(instance.username).data
        return response



class Post_serializer_get(serializers.ModelSerializer):
    class Meta:
        model=post
        fields='__all__'
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['content']=Post_Content_serializer(instance.Post_Content).data
        response['user']=ClientSerializer_update(instance.User).data


        return response


class Like_serializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields='__all__'


class UnLike_serializer(serializers.ModelSerializer):
    class Meta:
        model=UnLike
        fields='__all__'
