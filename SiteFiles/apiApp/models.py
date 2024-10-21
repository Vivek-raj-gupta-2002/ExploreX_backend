from django.db import models
import uuid
from django.conf import settings

def user_directory_path(instance, filename):
    # Generate a unique alphanumeric identifier using uuid
    unique_id = uuid.uuid4().hex  # Generates a unique 32-character hex string

    # Get the file extension
    extension = filename.split('.')[-1]

    # Create a new filename with the unique id and original file extension
    new_filename = f'{unique_id}.{extension}'

    # File will be uploaded to MEDIA_ROOT/user_<username>/<unique_id>.<extension>
    return f'user_{instance.user.username}/{new_filename}'

class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    image = models.FileField(upload_to=user_directory_path)  # Use callable here for unique path
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.user.username}'

class Notes(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date = models.DateField(auto_created=True)
    note = models.TextField()

    def __str__(self):
        return "Note on '" + str(self.date) + "' by '" + str(self.user.username) + "'"

    class Meta:
        unique_together = ('user', 'date')


# model for good and bad things of the day
class GoodBad(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    good = models.CharField(max_length=100)
    bad = models.CharField(max_length=100)
    date = models.DateField(auto_created=True)

    def __str__(self):
        return str(self.date) + " : " + str(self.user.username)

    class Meta:
        unique_together = ('user', 'date')

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    
    bio = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)  # Add Date of Birth (DOB)

    # 5 good habits
    good_habit_1 = models.CharField(max_length=100, blank=True, null=True)
    good_habit_2 = models.CharField(max_length=100, blank=True, null=True)
    good_habit_3 = models.CharField(max_length=100, blank=True, null=True)
    good_habit_4 = models.CharField(max_length=100, blank=True, null=True)
    good_habit_5 = models.CharField(max_length=100, blank=True, null=True)

    # 5 bad habits
    bad_habit_1 = models.CharField(max_length=100, blank=True, null=True)
    bad_habit_2 = models.CharField(max_length=100, blank=True, null=True)
    bad_habit_3 = models.CharField(max_length=100, blank=True, null=True)
    bad_habit_4 = models.CharField(max_length=100, blank=True, null=True)
    bad_habit_5 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user.email} Profile'
