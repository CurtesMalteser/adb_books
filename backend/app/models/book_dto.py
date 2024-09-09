import os
from flask_migrate import Migrate
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column

username = os.environ.get('USER') or os.environ.get('USERNAME')
db_path = os.environ.get('DB_PATH')
db_path = db_path.replace('USER', username)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=db_path):
    with app.app_context():
      app.config["SQLALCHEMY_DATABASE_URI"] = database_path
      app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
      db.init_app(app)

      migrate = Migrate(app, db)  # Initialize Flask-Migrate

      with app.app_context():
        db.create_all()

'''
BookDto
'''
class BookDto(db.Model):  
  __tablename__ = 'books'

  id = Column(Integer, primary_key=True)
  isbn13 = mapped_column(String, nullable=False, unique=True)
  title = mapped_column(String, nullable=False)
  author = mapped_column(String, nullable=False)
  image = db.Column(String, nullable=True, default=None)
  shelf = db.Column(String, nullable=True, default=None)

  def __init__(self, isbn13, title, author, image, shelf):
    self.isbn13 = isbn13
    self.title = title
    self.author = author
    self.image = image
    self.shelf = shelf


  def insert(self):
      db.session.add(self)
      db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

