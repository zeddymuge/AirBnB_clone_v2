#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from models.review import Review
from os import getenv


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay
    Attributes:
        city_id:
        user_id:
        name:
        description:
        number_rooms:
        number_bathrooms:
        max_guest:
        price_by_night:
        latitude:
        longitude:
        """
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

    reviews = relationship('Review', backref='place', cascade='delete')
    amenities = relationship("Amenity", secondary=place_amenity,
                             backref='place-amenities',
                             viewonly=False)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """returns the list of Review instances with"""
            from model import storage
            rev = storage.all(Review)
            new_list = []

            for value in rev.values():
                if value[place_id] == self.id:
                    new_list.append(value)
            return new_list

        @property
        def amenities(self):
            """ Returns list of amenity ids """
            from models import storage
            objs = storage.all(Amenity)
            new_list = []

            for value in objs.values():
                if value.id in self.amenity_ids:
                    new_list.append(value)
            return new_list

        @amenities.setter
        def amenities(self, value):
            """ Appends amenity ids"""
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
