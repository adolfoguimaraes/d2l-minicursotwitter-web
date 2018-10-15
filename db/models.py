from sqlalchemy import Column, Integer, String, Text, BIGINT, DATETIME
from db.database import Base


class AllTweets(Base):

    __tablename__ = "AllTweets"

    id = Column(Integer, primary_key=True,autoincrement=True)
    tweet_id = Column(String, unique=True)
    user = Column(BIGINT)
    text = Column(Text)
    date = Column(DATETIME)
    rt_user = Column(Text)
    query = Column(Text)
    context = Column(Text)

    def __init__(self, tweet_id=None, user=None, text=None, date=None, rt_user=None, query=None, context=None):
        self.tweet_id = tweet_id
        self.user = user
        self.text = text
        self.date = date
        self.rt_user = rt_user
        self.context = context
        self.query = query


class UsuariosRT(Base):
    __tablename__ = 'usuarios_rt'
    id = Column(Integer, primary_key=True,autoincrement=True)
    usuario = Column(Text, unique=True)
    frequencia = Column(Integer, unique=False)

    def __init__(self, usuario=None, frequencia=None):
        self.usuario = usuario
        self.frequencia = frequencia

    def __repr__(self):
        return '<Usuario %r>' % (self.usuario)


class Termos(Base):
    __tablename__ = 'termos'
    id = Column(Integer, primary_key=True,autoincrement=True)
    termo = Column(Text, unique=True)
    frequencia = Column(Integer, unique=False)

    def __init__(self, termo=None, frequencia=None):
        self.termo = termo
        self.frequencia = frequencia

    def __repr__(self):
        return '<Termo %r>' % (self.termo)


class UsuariosCitados(Base):
    __tablename__ = 'usuarios_citados'
    id = Column(Integer, primary_key=True,autoincrement=True)
    usuario = Column(Text, unique=True)
    frequencia = Column(Integer, unique=False)

    def __init__(self, usuario=None, frequencia=None):
        self.usuario = usuario
        self.frequencia = frequencia

    def __repr__(self):
        return '<Usuario %r>' % (self.usuario)


class HashtagsGraph(Base):
    __tablename__ = "hashtags_graph"

    id = Column(Integer, primary_key=True,autoincrement=True)
    hashtag = Column(Text, unique=False)
    frequencia = Column(Integer, unique=False)
    date = Column(DATETIME)
    context = Column(Text)

    def __init__(self, hashtag=None, frequencia=None, date=None, context=None):
        self.hashtag=hashtag
        self.frequencia=frequencia
        self.date=date
        self.context=context

    def __repr__(self):
        return '<Hashtag %r>' % (self.hashtag)


class Hashtags(Base):
    __tablename__ = 'hashtags'
    id = Column(Integer, primary_key=True,autoincrement=True)
    hashtag = Column(Text, unique=True)
    frequencia = Column(Integer, unique=False)

    def __init__(self, hashtag=None, frequencia=None):
        self.hashtag = hashtag
        self.frequencia = frequencia

    def __repr__(self):
        return '<Hashtag %r>' % (self.hashtag)


class BigramTrigram(Base):
    __tablename__ = 'bigram_trigram'

    id = Column(Integer, primary_key=True,autoincrement=True)
    text = Column(Text)
    tipo = Column(Integer)

    def __init__(self, text=None, tipo=None):
        self.text = text
        self.tipo = tipo

    def __repr__(self):
        return '<BigramTrigram %r>' % (self.text)