from celery import shared_task


@shared_task
def normal_trigger() -> None:
    print("hello")