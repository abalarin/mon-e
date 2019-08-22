from MonE import db, ma, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    join_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# -- Schemas --
class UserSchema(ma.Schema):
    class Meta:
        fields = ("first_name", "last_name", "username", "password", "email", "admin", "join_date")
