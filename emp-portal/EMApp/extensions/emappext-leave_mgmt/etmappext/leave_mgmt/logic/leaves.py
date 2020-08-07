import logging

log = logging.getLogger(__name__)


def leave_create(app_context, data_dict):
    """
    Api action leaves create. Employee can apply for leave and it will go to the pending state
    before getting approved by the re4porting manager.
    :param app_context: dict (Application context)
    :param data_dict: dict (data dictionary)
    :return: dict
    """
    pass

def leave_update(app_context, data_dict):
    """
    Leaves update - this allows to change the status of the leaves, and
    also leave can be withdrawn only if its status is pending.
    i.e.
        - Employee can withdraw the applied leaves
        - Approver can approve or reject leaves
        - Approver should add comments before rejecting the leave.
    :param app_context: dict (Application context)
    :param data_dict: dict (data dictionary)
    :return: dict
    """
    pass

def leaves_show(app_context, data_dict):
    """
    leave show given leave id
    :param app_context: dict (Application/user context)
    :param data_dict: dict (data dictionary)
    :return: dict
    """
    pass
