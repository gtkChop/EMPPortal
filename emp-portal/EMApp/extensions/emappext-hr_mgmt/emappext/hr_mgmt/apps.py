from django.apps import AppConfig


class EMAppExtHRConfig(AppConfig):
    """
    Core Employee Task Management Config process.

    Attributes:
        name: name of the plugin
        verbose_name: Label
    Methods:
        ready: This is where app collects information from all the installed apps/plugins
    """
    name = 'emappext.hr_mgmt'
    verbose_name = "HR employee management extension - base employee model"
    label = "hr_mgmt"
