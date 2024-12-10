from datetime import datetime, timezone
from typing import Optional

from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), index = True, unique = True)
    email : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), index = True, unique = True)  

