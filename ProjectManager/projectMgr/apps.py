from django.apps import AppConfig


class ProjectMgrConfig(AppConfig):
    name = 'projectMgr'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('User'))
        registry.register(self.get_model('Project'))
        registry.register(self.get_model('TaskGroup'))
        registry.register(self.get_model('Task'))