from datetime import date
from django.contrib.auth.models import User
from apiApp.models import GoodBad, Notes, UserProfile
from chatApp.models import AIMessages, Message
from AgentApp.models import UserSummary


class UserSummaryInfo:
    def __init__(self, target_date, username=None):
        self.username = username
        self.target_date = target_date
    
    def get_last_summary(self, user):
        try:
            return UserSummary.objects.filter(user=user, date__lt=self.target_date).latest('date')
        except UserSummary.DoesNotExist:
            return None

    def get_user(self):
        try:
            return User.objects.get(username=self.username)
        except User.DoesNotExist:
            return None

    def get_goodbad(self, user):
        try:
            return GoodBad.objects.get(user=user, date=self.target_date)
        except GoodBad.DoesNotExist:
            return None

    def get_notes(self, user):
        try:
            return Notes.objects.get(user=user, date=self.target_date)
        except Notes.DoesNotExist:
            return None

    def get_user_profile(self, user):
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return None

    def get_ai_messages(self, user):
        return AIMessages.objects.filter(user=user, timestamp__date=self.target_date)

    def get_chat_messages(self, user):
        return Message.objects.filter(sender=user, timestamp__date=self.target_date)

    def generate_summary(self):
        user = self.get_user()
        if not user:
            return None  # No user found

        # Fetch related data
        goodbad = self.get_goodbad(user)
        notes = self.get_notes(user)
        profile = self.get_user_profile(user)
        ai_messages = self.get_ai_messages(user)
        chat_messages = self.get_chat_messages(user)
        last_summary = self.get_last_summary(user)  # Retrieve last summary

        # If no profile and no relevant data is found, return None
        if not (profile or goodbad or notes or ai_messages.exists() or chat_messages.exists() or last_summary):
            return None  # No data to generate summary

        # Prepare summary
        summary = ""

        if profile:
            summary += f"Profile Information:\n"
            summary += f"Bio: {profile.bio}\n"
            summary += f"DOB: {profile.dob}\n"
            summary += "Good Habits:\n"
            summary += f"  1. {profile.good_habit_1}\n  2. {profile.good_habit_2}\n"
            summary += f"  3. {profile.good_habit_3}\n  4. {profile.good_habit_4}\n"
            summary += f"  5. {profile.good_habit_5}\n"
            summary += "Bad Habits:\n"
            summary += f"  1. {profile.bad_habit_1}\n  2. {profile.bad_habit_2}\n"
            summary += f"  3. {profile.bad_habit_3}\n  4. {profile.bad_habit_4}\n"
            summary += f"  5. {profile.bad_habit_5}\n"

        if goodbad:
            summary += f"Good and Bad Things on {self.target_date}:\n"
            summary += f"Good: {goodbad.good}\n"
            summary += f"Bad: {goodbad.bad}\n\n"

        if notes:
            summary += f"Notes\n"

        if ai_messages.exists():
            summary += f"\nAI Conversations\n"
            for ai_msg in ai_messages:
                summary += f"  User: {ai_msg.message}\n"
                summary += f"  AI: {ai_msg.reply}\n"

        if chat_messages.exists():
            summary += f"\nChat Messages on {self.target_date}:\n"
            for chat_msg in chat_messages:
                summary += f"  User: {chat_msg.content}\n"

        if last_summary:
            summary += f"\nLast Summary on {last_summary.date}:\n{last_summary.summary}\n Give something different from this now"

        return summary