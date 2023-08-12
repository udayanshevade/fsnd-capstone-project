from db import db


class Model():
    """Abstraction for simple helper methods for models"""
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Movie(db.Model, Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.Text())

    def __repr__(self):
        return '<Movie ID: {}, title: {}, complete: {}>'.format(
            self.id,
            self.title,
            self.complete
        )

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
        }


class Actor(db.Model, Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    birthdate = db.Column(db.Date)

    def __repr__(self):
        return '<Actor ID: {}, name: {}, birthdate: {}>'.format(
            self.id,
            self.name,
            self.birthdate
        )

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'birthdate': self.birthdate,
        }
