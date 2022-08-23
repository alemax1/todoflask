from src import db


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=True)
    time_start = db.Column(db.String(128), nullable=True)
    time_finish = db.Column(db.String(128), nullable=True)
    description = db.Column(db.Text)
    complete = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False, index=True)

    def __init__(self, title, time_start, time_finish, description, complete, category_id):
        self.title = title
        self.time_start = time_start
        self.time_finish = time_finish
        self.description = description
        self.complete = complete
        self.category_id = category_id

    def __repr__(self):
        return f'Task({self.title}, {self.time_start}, {self.time_finish}, {self.complete})'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'time_start': self.time_start,
            'time_finish': self.time_finish,
            'complete': self.complete,
            'category_id': self.category_id
        }


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(60), nullable=True)

    def __init__(self, category):
        self.category = category

    def __repr__(self):
        return f'Category({self.category})'

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
        }