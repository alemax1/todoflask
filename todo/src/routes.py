from flask import request
from flask_restful import Resource

from src import api, db
from src.models import Task, Category


class Smoke(Resource):
    def get(self):
        return {'message': 'ok'}, 200


class TaskListApi(Resource):
    def get(self, id=None):
        if not id:
            tasks = db.session.query(Task).all()
            return [t.to_dict() for t in tasks], 200
        task = db.session.query(Task).filter_by(id=id).first()
        if not task:
            return '', 404
        return task.to_dict(), 200

    def post(self):
        task_json = request.json
        ids = [id[0] for id in Category.query.with_entities(Category.id).all()]
        if not task_json:
            return {'message': 'Wrong data'}, 400
        if task_json['category_id'] not in ids:
            return {'message': 'Wrong category_id for your task'}
        try:
            task = Task(
                title=task_json['title'],
                time_start=task_json['time_start'],
                time_finish=task_json['time_finish'],
                description=task_json.get('description'),
                complete=task_json.get('complete'),
                category_id=task_json['category_id'],
            )
            db.session.add(task)
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Created successfully'}, 201

    def put(self, id):
        task_json = request.json
        if not task_json:
            return {'message': 'Wrong data'}, 400
        try:
            db.session.query(Task).filter_by(id=id).update(
                dict(
                    title=task_json['title'],
                    time_start=task_json['time_start'],
                    time_finish=task_json['time_finish'],
                    description=task_json.get('description'),
                    complete=task_json.get('complete'),
                    category_id=task_json['category_id'],
                )
            )
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Updated successfully'}, 201

    def patch(self, id):
        task = db.session.query(Task).filter_by(id=id).first()
        if not task:
            return '', 404
        task_json = request.json
        title = task_json.get('title'),
        time_start = task_json.get('time_start'),
        time_finish = task_json.get('time_finish'),
        description = task_json.get('description'),
        complete = task_json.get('complete'),
        category_id = task_json.get('category_id')
        if title:
            task.title = title
        elif time_start:
            task.time_start = time_start
        elif time_finish:
            task.time_finish = time_finish
        elif description:
            task.description = description
        elif complete:
            task.complete = complete
        elif category_id:
            task.category_id = category_id

        db.session.add(task)
        db.session.commit()
        return {'message': 'Updated successfully'}, 201

    def delete(self, id):
        task = db.session.query(Task).filter_by(id=id).first()
        if not task:
            return '', 404
        db.session.delete(task)
        db.session.commit()
        return '', 204


class CategoryListApi(Resource):
    def get(self, id=None):
        if not id:
            categories = db.session.query(Category).all()
            return [c.to_dict() for c in categories], 200
        category = db.session.query(Category).filter_by(id=id).first()
        if not category:
            return '', 404
        return category.to_dict(), 200

    def post(self):
        category_json = request.json
        if not category_json:
            return {'message': 'Wrong data'}, 400
        try:
            category = Category(
                category=category_json['category'],
            )
            db.session.add(category)
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Created successfully'}, 201

    def put(self, id):
        category_json = request.json
        if not category_json:
            return {'message': 'Wrong data'}, 400
        try:
            db.session.query(Category).filter_by(id=id).update(
                dict(
                    category=category_json['category'],
                )
            )
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Updated successfully'}, 201

    def patch(self, id):
        category = db.session.query(Category).filter_by(id=id).first()
        if not category:
            return '', 404
        category_json = request.json
        category = category_json.get('category')
        if category:
            category.category = category

        db.session.add(category)
        db.session.commit()
        return {'message': 'Updated successfully'}, 201

    def delete(self, id):
        category = db.session.query(Category).filter_by(id=id).first()
        if not category:
            return '', 404
        db.session.delete(category)
        db.session.commit()
        return '', 204


api.add_resource(Smoke, '/smoke', strict_slashes=False)
api.add_resource(TaskListApi, '/tasks', '/tasks/<id>', strict_slashes=False)
api.add_resource(CategoryListApi, '/categories', '/categories/<id>', strict_slashes=False)
