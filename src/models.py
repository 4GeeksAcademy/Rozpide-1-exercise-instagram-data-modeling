import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import create_engine
from eralchemy2 import render_er
# declaro la base de datos y la conexión a la misma de la cual heredarán las clases
Base = declarative_base()
# clase Person que hereda de Base y que representa la tabla person
class Person(Base):
    __tablename__ = 'person' # nombre de la tabla en la base de datos Person es el nombre de la tabla pero en singular y en minúsculas
    id = Column(Integer, primary_key=True) # columna id de tipo entero y clave primaria que representa el id de la persona
    name = Column(String(250), nullable=False) # columna name de tipo string de 250 caracteres y no puede ser nulo que representa el nombre de la persona
# clase Address que hereda de Base y que representa la tabla address que tiene una relación con la tabla person por medio de la columna person_id
class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True) # columna id de tipo entero y clave primaria que representa el id de la dirección
    street_name = Column(String(250)) # columna street_name de tipo string de 250 caracteres que representa el nombre de la calle
    street_number = Column(String(250)) # columna street_number de tipo string de 250 caracteres que representa el número de la calle
    post_code = Column(String(250), nullable=False) # columna post_code de tipo string de 250 caracteres y no puede ser nulo que representa el código postal
    person_id = Column(Integer, ForeignKey('person.id')) # columna person_id de tipo entero que representa el id de la persona y es una clave foránea que se relaciona con la columna id de la tabla person
    person = relationship(Person) # relación con la tabla person
 # clase NombreUsuario que hereda de Base y que representa la tabla nombre_usuario que tiene una relación con la tabla person por medio de la columna person_id y con la tabla address por medio de la columna address_id    
class NombreUsuario(Base):
    __tablename__ = 'nombre_usuario'
    id = Column(Integer, primary_key=True)
    address = relationship('Address') # relación con la tabla address
    address_id = Column (Integer, ForeignKey('address.id')) # columna address_id de tipo entero que representa el id de la dirección y es una clave foránea que se relaciona con la columna id de la tabla address
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False) # columna person_id de tipo entero y no puede ser nulo que representa el id de la persona y es una clave foránea que se relaciona con la columna id de la tabla person
    person = relationship('Person', back_populates='nombre_usuario') # relación con la tabla person 
    posts = relationship('Post', back_populates='usuario') # relación con la tabla post 
    
Person.nombre_usuario = relationship('NombreUsuario', uselist=False, back_populates='person') # define inversamente la relación entre la tabla person y la tabla nombre_usuario
# clase post que representa la tabla post con sus distintas relaciones    
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('nombre_usuario.id'), nullable=False)
    usuario = relationship('NombreUsuario', back_populates='posts')
    title = Column(String(250), nullable=False)
    content = Column('Texto', nullable=False)
    media = relationship('Media', back_populates='post')
    comments = relationship('Comment', back_populates='post')
    likes = relationship('MeGusta', back_populates='post')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship('Post', back_populates='media')
    likes = relationship('MeGusta', back_populates='media')
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('nombre_usuario.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    author = relationship('NombreUsuario', back_populates='comments')
    post = relationship('Post', back_populates='comments')
    likes = relationship('MeGusta', back_populates='comment')
class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('nombre_usuario.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('nombre_usuario.id'), primary_key=True)
    follower = relationship('NombreUsuario', foreign_keys=[user_from_id], back_populates='following')
    followed = relationship('NombreUsuario', foreign_keys=[user_to_id], back_populates='followers')
## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
