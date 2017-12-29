from __future__ import absolute_import, unicode_literals

import base64
import datetime

from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from orme.db import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String)

    def __repr__(self):
        return "<User(email='%s', password_hash='%s')>" % (self.email, self.password_hash)

    @staticmethod
    def encode_password(password):
        """Encode password (using base64 algorithm)

        Args
            password (str): the password

        Returns
            hashed password string

        """
        return base64.b64encode(password.encode('utf-8')).decode('utf-8')

    @staticmethod
    def decode_password(password_hash):
        """Decode the encoded password (using base64 algorithm)

        Args
            password_hash (str) base64-encodded password string

        Returns
            password string

        Raises
            binascii.Error exception is raised if s is incorrectly padded.

        """
        return base64.b64decode(password_hash).decode('utf-8')


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True)
    balance = Column(Integer, default=0)
    currency = Column(Enum('bitcoin', 'ethereum', name='currency_types'))
    wallet_type = Column(Enum('orv', 'user', name='wallet_types'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow())
    password = Column(String)
    # TODO: Add private key field
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")


User.addresses = relationship("Address", order_by=Address.id, back_populates="user")


class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String(255), unique=True, nullable=False)
    abi = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow())


class AddressSchema(ModelSchema):
    class Meta:
        model = Address


class UserSchema(ModelSchema):
    id = fields.Integer()
    email = fields.Email()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    addresses = fields.Nested(AddressSchema, only=('address', 'balance', 'currency', 'password'), many=True)


class ContractSchema(ModelSchema):
    class Meta:
        model = Contract

# Do not create all using metadata, since structure is created via Alembic migrations
# Base.metadata.create_all(engine)

# test_user = User(email='123@example.com', password_hash=User.encode_password('123456'))
# db.session.add(test_user)
# db.session.commit()
#
# query = db.session.query(User)
# print(query.all())
