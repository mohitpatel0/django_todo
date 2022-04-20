from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class TaskData(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    task_id =models.IntegerField()
    task_name =models.CharField(max_length=200)
    task_details =models.TextField()
    task_created_date =models.DateField(auto_now_add=True)
    test_created_time =models.TimeField(auto_now_add=True)
    task_end_date =models.DateField()
    task_end_time =models.TimeField()
    is_complete=models.BooleanField(default=False)

    def __str__(self):
        return str(self.task_id)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)        