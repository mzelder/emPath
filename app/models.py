from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# modale do zwrotu
class User(db.Model):
    __tablename__ = "users"
    userId = db.Column(db.Integer, primary_key=True) #Identyfikator użytkownika
    birthYear = db.Column(db.Integer, nullable=False) #Rok urodzenia użytkownika.
    sex = db.Column(db.Enum('F', 'M'), nullable=False) #Płeć metrykalna w momencie narodzin. F or M
    placeOfResidence = db.Column(db.String(50), nullable=False) # village < 20 tys, town - 20-100 tys, city > 100 tys
    additionalInformation = db.Column(db.String(500), nullable=True) #Opcjonalne. Dodatkowe informacje o użytkowniku. Np. zawód, wykształcenie, przebyte choroby.
    #training_sessions = db.relationship("Training_Session", backref="user", lazy=True)

#class Resource(db.Model):
#    __tablename__ = "resources"
#    resourceId = db.Column(db.Integer, primary_key=True) #Identyfikator zasobu.
#    type = db.Column(db.Enum('image', 'video', 'text', 'audio','other'), nullable=False) #Typ zasobu. Możliwe wartości: image, video, text, audio oraz other.
#    emotions = db.Column(db.Enum('neutral', 'joy', 'disgust', 'surprise', 'fear', 'sadness', 'anger'), nullable=False) #Emocje, które prezentuje zasób.
#    age = db.Column(db.String(50), nullable=True) #Opcjonalne. Wiek osoby pokazanej na zasobie.
#    imageCategory = db.Column(db.Enum('face', 'full-body'), nullable=False) #Opcjonalne, ale wymagane dla obrazów. Kategoria obiektu przedstawianego przez zasób. Możliwe wartości to: face albo full-body.
#    training_sessions = db.relationship("Training_Session", backref="resource", lazy=True)

class Training_Session_Result(db.Model):
    __tablename__ = "training_session_result"
    resultId = db.Column(db.Integer, primary_key=True) #Identyfikator wyniku ćwiczenia.
    userId = db.Column(db.Integer, db.ForeignKey("users.userId"), nullable=False)
    #sessionId = db.Column(db.Integer, db.ForeignKey('training_sessions.sessionId'), nullable=False)
    #resourceId = db.Column(db.Integer, db.ForeignKey('resources.resourceId'), nullable=False)
    #recognizedEmotion = db.Column(db.Enum('neutral', 'joy', 'disgust', 'surprise', 'fear', 'sadness', 'anger'), nullable=False) #Emocja rozpoznawana przez użytkownika.
    startedAt = db.Column(db.DateTime(), nullable=False) #Data i czas rozpoczęcia sesji treningowej.
    endedAt = db.Column(db.DateTime(), nullable=False) #Data i czas zakończenia sesji treningowej.
    type = db.Column(db.Enum('diagnosis', 'training'), nullable=False)
    score = db.Column(db.Integer, nullable = False)

class UserServer(db.Model):
    __tablename__ = "login_validation"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    type = db.Column(db.Enum('user', 'scientist'))
    userId = db.Column(db.Integer, db.ForeignKey("users.userId"), nullable=True)
