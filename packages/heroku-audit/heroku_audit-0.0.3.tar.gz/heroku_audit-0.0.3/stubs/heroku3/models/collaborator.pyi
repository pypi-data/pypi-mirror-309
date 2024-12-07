import datetime
from typing import Optional

from . import User

class Collaborator:
    created_at: datetime.datetime
    user: User

    # HACK: https://github.com/martyzz1/heroku3.py/pull/133
    role: Optional[str]
