admin = {"ajlozier": "U1F2H84FM", "be_humble": "U0MP7J9D5", "zeke": "U0G873FP0", "stewart": "U3EKAT8R1"}
qa = {"ben.rogers": "U0N0S52P4", "exact0ninja": "U0R0NUC84"}


def is_admin(slack_id):
    if slack_id in admin.values():
        return True
    else:
        return False


def is_qa(slack_id):
    if slack_id in qa.values():
        return True
    else:
        return False
