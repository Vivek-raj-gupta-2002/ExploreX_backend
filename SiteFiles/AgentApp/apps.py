from django.apps import AppConfig


class AgentappConfig(AppConfig):
    name = 'AgentApp'

    def ready(self):
        from .tasks import normal_trigger, getSummary
        # getSummary()