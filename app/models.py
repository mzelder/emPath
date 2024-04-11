from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# modale do zwrotu
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    birthYear = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    placeOfResidence = db.Column(db.String(50), nullable=False) # village < 20 tys, town - 20-100 tys, city > 100 tys
    additionalInformation = db.Column(db.String(100), nullable=False) # student, employed, unemployed, retired
    training_sessions = db.relationship("Training_Session", backref="user", lazy=True)

class Training_Session(db.Model):
    __tablename__ = "training_sessions"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Typ sesji treningowej. Możliwe wartości:
    # diagnosis lub training. Gdzie diagnoza
    # rozumiana jest jako pierwsza sesja
    type = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    startedAt = db.Column(db.String(50), nullable=False)
    endedAt = db.Column(db.String(50), nullable=False)

class Resource(db.Model):
    __tablename__ = "resources"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    training_sessions = db.relationship("Training_Session", backref="resource", lazy=True)


class UserServer(db.Model):
    __tablename__ = "login_validation"
    id = db.Column(db.Integer, db.ForeignKey("users.id") primary_key = True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    type = db.Column(db.Enum('regular user', 'scientist'))
