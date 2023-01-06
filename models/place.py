#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.sql.schema import Table
from sqlalchemy.orm import relationship
from os import getenv

metadata = Base.metadata
place_amenity = Table(
    'place_amenity', metadata,
    Column(
        'place_id', String(60), ForeignKey('places.id'),
        primary_key=True, nullable=False),
    Column(
        'amenity_id', String(60), ForeignKey('amenities.id'),
        primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ Class Place Containing the most basic info """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship('Review', backref='place')
    amenities = relationship(
        "Amenity", secondary=place_amenity, viewonly=False,
        backref='places')
    if getenv("HBNB_TYPE_STORAGE") == "file":
        @property
        def reviews(self):
            """Getter of the review attribute"""
            from models import storage
            new_list = []
            for key, obj_rev in storage.all(Review).items():
                if obj_rev.place_id == self.id:
                    new_list.append(obj_rev)
            return new_list

        @property
        def amenities(self):
            """Getter of the amenity attribute"""
            from models.amenity import Amenity
            from models import storage
            new_list = []
            for key, obj_amenity in storage.all(Amenity).items():
                if obj_amenity.id == self.amenity_ids:
                    new_list.append(obj_amenity)
            return new_list

        @amenities.setter
        def amenities(self, obj):
            """Setter to add an Amenity object"""
            from models.amenity import Amenity
            if type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
