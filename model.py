import config
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

from flask.ext.login import UserMixin

ENGINE = create_engine("sqlite:///allYourDatabaseAreBelongToMeme.db", echo=False) 
session = scoped_session(sessionmaker(bind=ENGINE,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

#############################################################
################## Class Declarations Here ##################
#############################################################


# Insert Class for Memes
class Meme(Base):
    """Create table to hold all meme images from web crawler"""
    __tablename__ = "memes"
    id = Column(Integer, primary_key = True)
    url = Column(String(500), nullable = True)
    #add in a timestamp object
    #timestamp = 

# Insert Class for Tags
class Tag(Base):
    """Create table to hold all possible tags from web crawler"""
    __tablename__ = "tags"
    id = Column(Integer, primary_key = True) 
    tag_name = Column(String(150), nullable = True)
    #add in a timestamp object
    #timestamp =        

# Insert Class for Users
class User(Base):
    """Create table to hold all user data"""
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    #add in a timestamp object
    #timestamp = 

# Insert Class for Corpus
class Corpus(Base):
    """Corpus will be the highlighted selection sent from the extension"""
    __tablename__ = "corpuses"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('User.id'))
    corpus = Column(String(1000), nullable = True)

    corpus_user = relationship("User",
        backref= backref("corpuses", order_by = id))

        
# Insert Class for Features
class Feature(Base):
    """Feature """
    __tablename__ = "features"
    id = Column(Integer, primary_key = True)
    feature = Column(String(64), nullable = True)
    tag_id  =  Column(Integer, ForeignKey('Tab.id'))
    frequency = Column(Integer, nullable = True)
    weight = Column(Integer, nullable = True)

    feature_tag = relationship("Tab",
        backref = backref("feature", order_by = id))

# Insert Class for Selections
class Selection(Base):
    """There will be notes here"""
    __tablename__ = "selections"
    id = Column(Integer, primary_key = True)
    feature_id = Column(Integer, ForeignKey('features.id'))
    meme_id = Column(Integer, ForeignKey('meme.id'))
    corpus_id = Column(Integer, ForeignKey('corpuses.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    user_selection = relationship("User",
        backref = backref("selections", order_by=id))

    feature_selection = relationship("Feature",
        backref = backref("selections", order_by=id))

    meme_selection = relationship("Meme",
        backref = backref("selections", order_by=id))

    corpus_selection = relationship("Corpus",
        backref = backref("selections", order_by=id))


#############################################################
##################### functions #############################
#############################################################

def createTables():
    Base.metadata.create_all(ENGINE)
    print "We created alll of the tabbbbbleeeehs."


def main():
    """In case we need this for something."""
    createTables()


if __name__ == "__main__":
    main()




