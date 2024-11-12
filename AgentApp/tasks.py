from celery import shared_task
from .models import UserSummary
from django.contrib.auth.models import User
from uttils import userSummary, summarizer
from datetime import datetime, timedelta

# Initialize the TextAnalyzer, you can set `use_azure=True` or `False` as per your requirement.
# For example, use Azure for this instance
textAnalyzer = summarizer.TextAnalyzer(use_azure=True)

def getSummary():
    # Fetch all users
    req_users = User.objects.all()

    # Calculate the date one day before the current date
    date = datetime.now() - timedelta(days=1)

    # Create a UserSummary instance
    summ = userSummary.UserSummaryInfo(date)

    # Iterate over the users to generate the summary
    for user in req_users:
        summ.username = user.username
        summary = summ.generate_summary()  # Generate a raw summary for the user

        if summary:
            try:
                # First, use the TextAnalyzer to summarize the text
                summarized_text = textAnalyzer.summarize_text(summary)

                # Initialize a dictionary to store the fields to be updated
                defaults = {}

                # Add summarized_text if it's available
                if summarized_text:
                    defaults['summary'] = summarized_text

                    # Now analyze personality, mood, and tasks based on the summary (optional)
                    personality = textAnalyzer.analyze_personality(summarized_text)
                    mood = textAnalyzer.describe_mood(summarized_text)
                    tasks = textAnalyzer.suggest_tasks(summarized_text)

                    # Add the fields to the defaults dictionary only if they are not None
                    if personality:
                        defaults['personality'] = personality
                    if mood:
                        defaults['mood'] = mood
                    if tasks:
                        defaults['task'] = tasks

                # Save whatever data is available in the `defaults` dictionary
                if defaults:  # Only update if there is something to save
                    UserSummary.objects.update_or_create(
                        user=user,
                        date=date.date(),  # Save the date as a date object
                        defaults=defaults
                    )
            except Exception as e:
                print(f"Error processing user {user.username}: {str(e)}")

    print('Summary generation and save complete!')

@shared_task
def normal_trigger() -> None:
    print("Task triggered!")
    # getSummary()
