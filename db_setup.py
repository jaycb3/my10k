import os
import sys
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50))
    password = Column(String(20))

    @property
    def serialize(self):
        """Return object data in serializable format"""
        return {
            'name':self.name,
            'id':self.id,
            'email':self.email,
            'password':self.password,
        }

class Record(Base):
    __tablename__ = 'record'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    subject = Column(String(10), nullable=False)
    start_time = Column(DateTime)
    stop_time = Column(DateTime)
    total_minutes = Column(Integer, default=0)
    goal = Column(Integer, default=None)
    comments = Column(String(1200), default="")

    @property
    def serialize(self):
        """Return object in serializable format."""
        return {
            'id':self.id,
            'person_id':self.person_id,
            'subject':self.subject,
            'start_time':self.start_time,
            'stop_time':self.stop_time,
            'total_minutes':self.total_minutes,
            'goal':self.goal,
            'comments':self.comments,
        }

engine = create_engine('sqlite:///records.db')

Base.metadata.create_all(engine)
