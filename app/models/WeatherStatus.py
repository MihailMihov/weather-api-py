from app.models import db


class WeatherStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    icon = db.Column(db.Text, nullable=False)
    background = db.Column(db.Text, nullable=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<WeatherStatus {self.description}>'
