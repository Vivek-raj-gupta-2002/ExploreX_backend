from django.db import models
from django.conf import settings

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
