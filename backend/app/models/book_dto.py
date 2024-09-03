import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column

username = os.environ.get('USER') or os.environ.get('USERNAME')
database_path = os.environ.get('DB_PATH')
database_path = database_path.replace('USER', username)

print(f'database_path: {database_path}')

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    with app.app_context():
      app.config["SQLALCHEMY_DATABASE_URI"] = database_path
      app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
      db.init_app(app)
      db.create_all()

'''
BookDto
'''
class BookDto(db.Model):  
  __tablename__ = 'books'

  id = Column(Integer, primary_key=True)
  bookId = mapped_column(String, nullable=False)
  title = mapped_column(String, nullable=False)
  author = mapped_column(String, nullable=False)
  rating = mapped_column(Integer, nullable=False)

  def __init__(self, bookId, title, author, rating):
    self.bookId = bookId
    self.title = title
    self.author = author
    self.rating = rating

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

