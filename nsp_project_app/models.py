from django.db import models
from  django.contrib.auth.models import User
# Create your models here.'


class State(models.Model):
    StateName = models.CharField(max_length=50,unique=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdateDate= models.DateTimeField(auto_now_add=True)





class Technical(models.Model):
    TechnicalName = models.CharField(max_length=250,unique=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdateDate= models.DateTimeField(auto_now_add=True)



class NonTechnical(models.Model):

    NonTechnicalName = models.CharField(max_length=250,unique=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdateDate= models.DateTimeField(auto_now_add=True)



class City(models.Model):
    CityName = models.CharField(max_length=50,unique=True)
    CityState = models.ForeignKey(State,on_delete=models.CASCADE)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdateDate= models.DateTimeField(auto_now_add=True)






class Institute(models.Model):
    #username=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    InstituteAddress = models.TextField(max_length=500)
    InstitutePhoneNo = models.IntegerField(unique=True)
    State_Name = models.ForeignKey(State,on_delete=models.CASCADE)
    city_Name = models.ForeignKey(City,on_delete=models.CASCADE)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdateDate= models.DateTimeField(auto_now_add=True)







class User_info(models.Model):
    img=models.ImageField(upload_to='media/img',blank=True,default=None)

    username=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=50 ,blank=True,null=True)
    email=models.EmailField(unique=True,null=True,blank=True)
    Institute = models.CharField(max_length=50 ,blank=True)
    TechnicalField = models.ForeignKey(Technical,None,blank=True,null=True)
    NonTechnicalField = models.ForeignKey(NonTechnical,None,blank=True,null=True)
    Age = models.IntegerField(default=0)
    State_Name = models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    city_Name = models.ForeignKey(City,on_delete=models.CASCADE,null=True,blank=True)
    BirthDate = models.DateField(null=True,blank=True)
    CreatedDate = models.DateField(auto_now_add=True)
    UpdateDate = models.DateField(auto_now_add=True)
    Job_Status = models.BooleanField(default=0)




class Content(models.Model):
    Post_Title = models.CharField(max_length=50,null=True,blank=True)

    Image = models.ImageField(null=True,blank=True)
    Text = models.TextField(null=True,blank=True)
    CreatedDate = models.DateField(auto_now_add=True)
    UpdateDate = models.DateField(auto_now_add=True)



class post(models.Model):
    User = models.ForeignKey(User_info,on_delete=models.CASCADE,null=True,blank=True)
    Post_Content = models.ForeignKey(Content,null=True,on_delete=models.CASCADE)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdateDate = models.DateField(auto_now_add=True)
    LikeCount = models.IntegerField(default=0)
    UnLikeCount = models.IntegerField(default=0)
    def to_dict(self):
        return {
            'User' : self.User,
            'Post_Content' : self.Post_Content,
            'CreatedDate' : self.CreatedDate,
            'UpdateDate' : self.UpdateDate,
            'LikeCount' : self.LikeCount,
            'UnLikeCount' : self.UnLikeCount,

}





class Like(models.Model):
    User = models.ForeignKey(User_info,on_delete=models.CASCADE,blank=True,null=True,)
    Post=models.ForeignKey(post,on_delete=models.CASCADE)
    LikeCount = models.IntegerField(default=0)



class UnLike(models.Model):
    User = models.ForeignKey(User_info,blank=True,null=True,on_delete=models.CASCADE)
    Post=models.ForeignKey(post,on_delete=models.CASCADE)
    UnLikeCount = models.IntegerField(default=0)



class Comment(models.Model):
    Post_comment = models.TextField()
    User = models.ForeignKey(User_info,on_delete=models.CASCADE,null=True,blank=True)
    Post = models.ForeignKey(post,on_delete=models.CASCADE)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdateDate= models.DateTimeField(auto_now_add=True)
#    flag = models.ChoiceField(racist,abusive)



class FriendRequest(models.Model):
    ToUser = models.ForeignKey(User_info,related_name='friendrequests',on_delete=models.CASCADE)
    FromUser = models.ForeignKey(User_info,related_name='Request_Sent',on_delete=models.CASCADE)
    Status = models.BooleanField(default=0)



class Followers_User(models.Model):
    User = models.ForeignKey(User_info,related_name='Followers',on_delete=models.CASCADE,null=True,blank=True)
    Followers = models.ForeignKey(User_info,on_delete=models.CASCADE,null=True,blank=True)



class Followig_User(models.Model):
    User = models.OneToOneField(User_info,related_name='Followings',on_delete=models.CASCADE)
    Following = models.ManyToManyField('self',blank=True)
