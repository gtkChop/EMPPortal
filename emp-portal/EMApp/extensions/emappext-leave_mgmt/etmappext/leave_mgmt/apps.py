from django.apps import AppConfig


class EMAppExtLeaveConfig(AppConfig):
    """
    Core Employee Leave Management Config process.

    Attributes:
        name: name of the plugin
        verbose_name: Label
    Methods:
        ready: This is where app collects information from all the installed apps/plugins
    """
    name = 'emappext.leave_mgmt'
    verbose_name = "Employee Leave Management Extension"
    label = "leave_mgmt"
