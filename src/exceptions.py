#src/exceptions.py
from enum import StrEnum


#region User

class UserIsNoneException(Exception):
    pass


class UsernameNotUniqueException(Exception):
    pass

#endregion


#region Sub

class SubIsNoneException(Exception):
    pass


class SubNameNotUniqueException(Exception):
    pass


class UserHasNoSubsException(Exception):
    pass

#endregion


#region Details for exceptions

class DetailsForHTTPExceptions(StrEnum):
    # User
    UserIsNoneException = "User not found"
    UserNameNotUniqueException = "The name should be unique"

    # Subscription
    SubIsNoneException = "Subscription not found"
    SubNameNotUniqueException = "The subscription name should be unique"
    UserHasNoSubsException = "User has no subscriptions"

#endregion
