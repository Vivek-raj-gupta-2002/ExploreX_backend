from rest_framework import serializers
from .models import UserProfile

{'email': 'vivekrajgupta2002@outlook.com', 'inputData': {'email': 'vivekrajgupta2002@outlook.com', 'bio': 'Vdhd', 'dob': '2024-09-29', 'bad_habit_1': 'Jdjd', 'bad_habit_2': 'Udhd', 'bad_habit_3': 'Jxjx', 'bad_habit_4': 'Udud', 'bad_habit_5': 'Uxux', 'good_habit_1': 'Hxjx', 'good_habit_2': 'Jxjx', 'good_habit_3': 'Hxhx', 'good_habit_4': 'Jdjd', 'good_habit_5': 'Jxjx'}}

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['email', 'bio', 'dob', 'good_habit_1', 'good_habit_2', 'good_habit_3', 'good_habit_4', 'good_habit_5',
                  'bad_habit_1', 'bad_habit_2', 'bad_habit_3', 'bad_habit_4', 'bad_habit_5']

    def create(self, validated_data):
        user = self.context['user']  # Get user from context
        return UserProfile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        # Update profile fields here
        instance.bio = validated_data.get('bio', instance.bio)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.good_habit_1 = validated_data.get('good_habit_1', instance.good_habit_1)
        instance.good_habit_2 = validated_data.get('good_habit_2', instance.good_habit_2)
        instance.good_habit_3 = validated_data.get('good_habit_3', instance.good_habit_3)
        instance.good_habit_4 = validated_data.get('good_habit_4', instance.good_habit_4)
        instance.good_habit_5 = validated_data.get('good_habit_5', instance.good_habit_5)
        instance.bad_habit_1 = validated_data.get('bad_habit_1', instance.bad_habit_1)
        instance.bad_habit_2 = validated_data.get('bad_habit_2', instance.bad_habit_2)
        instance.bad_habit_3 = validated_data.get('bad_habit_3', instance.bad_habit_3)
        instance.bad_habit_4 = validated_data.get('bad_habit_4', instance.bad_habit_4)
        instance.bad_habit_5 = validated_data.get('bad_habit_5', instance.bad_habit_5)
        instance.save()
        return instance
