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
    username = Column(String(250), nullable=False) # columna username de tipo string de 250 caracteres y no puede ser nulo que representa el nombre de usuario(Nickname)
    password = Column(String(250), nullable=False) # columna password de tipo string de 250 caracteres y no puede ser nulo que representa la contraseña del usuario
    address = relationship('Address') # relación con la tabla address
    address_id = Column (Integer, ForeignKey('address.id')) # columna address_id de tipo entero que representa el id de la dirección y es una clave foránea que se relaciona con la columna id de la tabla address
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False) # columna person_id de tipo entero y no puede ser nulo que representa el id de la persona y es una clave foránea que se relaciona con la columna id de la tabla person
    person = relationship('Person', back_populates='nombre_usuario') # relación con la tabla person 
    posts = relationship('Post', back_populates='usuario') # relación con la tabla post uno a muchos
    comments = relationship('Comment', back_populates='author') # relación con la tabla comment uno a muchos
    
Person.nombre_usuario = relationship('NombreUsuario', uselist=False, back_populates='person') # define inversamente la relación entre la tabla person y la tabla nombre_usuario
# clase post que representa la tabla post con sus distintas relaciones    
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)# columna id de tipo entero y clave primaria que representa el id del post
    user_id = Column(Integer, ForeignKey('nombre_usuario.id'), nullable=False)# columna user_id de tipo entero y no puede ser nulo que representa el id del usuario y es una clave foránea que se relaciona con la columna id de la tabla nombre_usuario
    usuario = relationship('NombreUsuario', back_populates='posts')# relación con la tabla nombre_usuario uno a muchos 
    title = Column(String(250), nullable=False) # columna title de tipo string de 250 caracteres y no puede ser nulo que representa el título del post 
    content = Column(Text, nullable=False) # columna content de tipo texto y no puede ser nulo que representa el contenido del post
    media = relationship('Media', back_populates='post') # relación con la tabla media uno a muchos 
    comments = relationship('Comment', back_populates='post') # relación con la tabla comment uno a muchos 
    likes = relationship('MeGusta', back_populates='post') # relación con la tabla me_gusta uno a muchos

class Media(Base):# clase media que representa la tabla media con sus distintas relaciones representando las imágenes o videos de los post
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True) # columna id de tipo entero y clave primaria que representa el id de la media
    url = Column(String(250), nullable=False) # columna url de tipo string de 250 caracteres y no puede ser nulo que representa la url de la media, puede ser la ruta de la imagen o video
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False) # columna post_id de tipo entero y no puede ser nulo que representa el id del post y es una clave foránea que se relaciona con la columna id de la tabla post
    post = relationship('Post', back_populates='media') # relación con la tabla post uno a muchos
    likes = relationship('MeGusta', back_populates='media') # relación con la tabla me_gusta uno a muchos
class Comment(Base): # clase comment que representa la tabla comment con sus distintas relaciones representando los comentarios de los post
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)# columna id de tipo entero y clave primaria que representa el id del comentario
    comment_text = Column(Text, nullable=False) # columna comment_text de tipo texto y no puede ser nulo que representa el texto del comentario
    author_id = Column(Integer, ForeignKey('nombre_usuario.id'), nullable=False) # columna author_id de tipo entero y no puede ser nulo que representa el id del autor del comentario y es una clave foránea que se relaciona con la columna id de la tabla nombre_usuario
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False) # columna post_id de tipo entero y no puede ser nulo que representa el id del post y es una clave foránea que se relaciona con la columna id de la tabla post
    author = relationship('NombreUsuario', back_populates='comments')# relación con la tabla nombre_usuario uno a muchos
    post = relationship('Post', back_populates='comments') # relación con la tabla post uno a muchos
    likes = relationship('MeGusta', back_populates='comment') # relación con la tabla me_gusta uno a muchos 
class Follower(Base): # clase follower que representa la tabla follower con sus distintas relaciones representando los seguidores de los usuarios 
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True) # columna id de tipo entero y clave primaria que representa el id del seguidor
    user_from_id = Column(Integer, ForeignKey('nombre_usuario.id'), primary_key=True)# columna user_from_id de tipo entero y clave primaria que representa el id del usuario que sigue y es una clave foránea que se relaciona con la columna id de la tabla nombre_usuario 
    user_to_id = Column(Integer, ForeignKey('nombre_usuario.id'), primary_key=True) # columna user_to_id de tipo entero y clave primaria que representa el id del usuario seguido y es una clave foránea que se relaciona con la columna id de la tabla nombre_usuario
    follower = relationship('NombreUsuario', foreign_keys=[user_from_id], back_populates='following') # relación con la tabla nombre_usuario uno a muchos tanto como seguidor como seguido, pero este es el seguidor
    followed = relationship('NombreUsuario', foreign_keys=[user_to_id], back_populates='followers') # relación con la tabla nombre_usuario uno a muchos tanto como seguidor como seguido, pero uno este es el seguido
    
# Clase MeGusta que representa la tabla me_gusta
class MeGusta(Base):
    __tablename__ = 'me_gusta'
    id = Column(Integer, primary_key=True)  # Clave primaria
    user_id = Column(Integer, ForeignKey('nombre_usuario.id'), nullable=False)  # Clave foránea que se relaciona con la tabla nombre_usuario
    post_id = Column(Integer, ForeignKey('post.id'))  # Clave foránea que se relaciona con la tabla post
    comment_id = Column(Integer, ForeignKey('comment.id'))  # Clave foránea que se relaciona con la tabla comment
    media_id = Column(Integer, ForeignKey('media.id'))  # Clave foránea que se relaciona con la tabla media
    usuario_id = Column(Integer, ForeignKey('nombre_usuario.id'))  # Clave foránea que se relaciona con la tabla nombre_usuario tanto como usuario como autor

    post = relationship('Post', back_populates='likes')  # Relación con la tabla post
    comment = relationship('Comment', back_populates='likes')  # Relación con la tabla comment
    media = relationship('Media', back_populates='likes')  # Relación con la tabla media
    
# Crear el motor de la base de datos y la sesión
engine = create_engine('sqlite:///:memory:')  # Crear una base de datos en memoria
Base.metadata.create_all(engine)  # Crear todas las tablas en la base de datos
Session = sessionmaker(bind=engine)  # Crear una clase de sesión
session = Session()  # Crear una instancia de sesión

# Crear un usuario con nombre de usuario
new_user = NombreUsuario(id=1, username='Jose Rózpide', password='123456') # Crear un usuario con nombre de usuario nuevo y añadirlo a la base de datos

# Crear publicaciones asociadas a este usuario
post1 = Post(id=101, user_id=1, title="Primer Post", content="Este es el contenido del primer post.")
post2 = Post(id=102, user_id=1, title="Segundo Post", content="Este es el contenido del segundo post.")

# Crear relaciones de seguimiento
seguimiento1 = Follower(id=1, user_from_id=1, user_to_id=2)# Crear un usuario con nombre de usuario nuevo y añadirlo a la base de datos
seguimiento2 = Follower(id=2, user_from_id=2, user_to_id=3)# Crear un usuario con nombre de usuario nuevo y añadirlo a la base de datos

# Añadir al usuario, sus publicaciones y relaciones de seguimiento a la sesión
session.add(new_user)# Añadir al nuevo usuario a la sesión de la base de datos que se creó
session.add(post1) # Añadir la publicación 1 a la sesión de la base de datos que se creó
session.add(post2) # Añadir la publicación 2 a la sesión de la base de datos que se creó
session.add(seguimiento1) # Añadir la relación de seguimiento 1 a la sesión de la base de datos que se creó
session.add(seguimiento2) # Añadir la relación de seguimiento 2 a la sesión de la base de datos que se creó

# Confirmar los cambios
session.commit() # Confirmar los cambios realizados en la sesión de la base de datos que se creó


    
## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png') # Generar el diagrama de la base de datos
    print("Success! Check the diagram.png file") # Imprimir un mensaje de éxito
except Exception as e: # Manejar cualquier excepción que ocurra
    print("There was a problem genering the diagram") # Imprimir un mensaje de error
    raise e # Lanzar la excepción que ocurrió para ver el error
