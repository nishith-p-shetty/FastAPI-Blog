from . import models

def get_all(db):
    return db.query(models.Blog).all()