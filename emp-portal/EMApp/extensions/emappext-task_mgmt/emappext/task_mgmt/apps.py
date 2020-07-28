from django.apps import AppConfig


class EMAppExtTaskProjectConfig(AppConfig):
    """
    Core Employee Task Management Config process.

    Attributes:
        name: name of the plugin
        verbose_name: Label
    Methods:
        ready: This is where app collects information from all the installed apps/plugins
    """
    name = 'emappext.task_mgmt'
    verbose_name = "Extension for employee task management"
    label = 'task_mgmt'
