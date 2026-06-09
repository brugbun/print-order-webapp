from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class _QueuedOrder(db.Model):
    __bind_key__ = "queued"
    __tablename__ = "queued"

    id = db.Column(db.Integer, primary_key=True)
    order_item = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Order {self.id} {self.name!r} is currently Queued>"

class _InProgressOrder(db.Model):
    __bind_key__ = "in_progress"
    __tablename__ = "in_progress"

    inprog_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    order_item = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Order {self.id} {self.name!r} is currently In Progress>"

class _RedoItemOrder(db.Model):
    __bind_key__ = "redo_item"
    __tablename__ = "redo_item"

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.String(120), nullable=False)
    finished = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        parent_order_item = db.session.get(RedoOrder, self.parent_id)
        finished = "True" if self.finished else "False"
        return f"<Order {self.id} {self.item_name} for parent {self.parent_id} {parent_order_item}. Finished: {finished}>"

class _RedoOrder(db.Model):
    __bind_key__ = "redo"
    __tablename__ = "redo"

    redo_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    order_item = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Order {self.id} {self.name!r} currently has keys queued for Redo>"

class _FinishedOrder(db.Model):
    __bind_key__ = "finished"
    __tablename__ = "finished"

    finished_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    order_item = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Order {self.id} {self.name!r} is currently Finished>"

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_BINDS"] = {
        "queued": "sqlite:///queued.db",
        "in_progress": "sqlite:///inprog.db",
        "redo_item": "sqlite:///redo_item.db",
        "redo": "sqlite:///redo.db",
        "finished": "sqlite:///finished.db"
    }

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

class Order():
    __db_class__ = None

    def pull_all():
        orders = db.session.execute(db.select(__db_class__).order_by(id))
        return orders

    def pull_one(id):
        order = db.session.get(__db_class__, id)
        return order

    def place(order_item):
        order = __db_class__(order_item=order_item)
        db.session.add(order)
        db.session.commit()

class Queued():
    __db_class__ = _QueuedOrder

    #def pull_all():

    #def pull_one(id):

    #def place():

class InProgress():
    __db_class__ = _InProgressOrder

    #def pull_all():

    #def pull_one(id):

    def place(id):
        order = db.session.get(_QueuedOrder, id)
        data = {k: v for k, v in order.__dict__.items() if not k.startswith("_")}

        db.session.delete(order)
        in_progress = __db_class__(**data)
        db.session.add(in_progress)
        db.session.commit()

class RedoItem():
    __db_class__ = _RedoItemOrder

    def place(id, item_name):
        order = __db_class__(id=parent_id, item_name=item_name, finished=False)
        db.session.add(order)
        db.session.commit()

class Redo():
    __db_class__ = _RedoOrder

    def place(id):
        order = db.session.get(_InProgressOrder, id)
        data = {k: v for k, v in order.__dict__.items() if not k.startswith("_")}

        db.session.delete(order)
        redo = __db_class__(**data)
        db.session.add(redo)
        db.session.commit()

class Finished():
    __db_class__ = _FinishedOrder

    def place(id):
        in_progress = db.session.get(_InProgressOrder, id)
        redo = db.session.get(_RedoOrder, id)

        order = in_progress or redo
        data = {k: v for k, v in order.__dict__.items() if not k.startswith("_")}

        db.session.delete(order)
        finished = __db_class__(**data)
        db.session.add(finished)
        db.session.commit()

#def pull_queued_orders():
    #orders = db.session.execute(db.select(Queued).order_by(id))
    #return orders

#def pull_inprog_orders():
    #orders = db.session.execute(db.select(InProgress).order_by(id))
    #return orders

#def pull_redo_orders():
    #orders = db.session.execute(db.select(Redo).order_by(id))
    #return orders

#def pull_finished_orders():
    #orders = db.session.execute(db.select(Finished).order_by(id))
    #return orders


