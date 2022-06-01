from app.models import db


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True, nullable=False)
    lat = db.Column(db.Float, index=True, nullable=False)
    lon = db.Column(db.Float, index=True, nullable=False)

    def __repr__(self):
        return f'<City {self.name}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_city(self):
        data = {
            'name': self.name
        }
        return data
