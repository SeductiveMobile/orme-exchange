import db
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import base64
import datetime


class User(db.Base):
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


class Address(db.Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True)
    balance = Column(Integer)
    currency = Column(Enum('bitcoin', 'ethereum', name='currency_types'))
    wallet_type = Column(Enum('orv', 'user', name='wallet_types'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow())
    password = Column(String)
    # TODO: Add private key field
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")


User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

db.Base.metadata.create_all(db.engine)

# test_user = User(email='123@example.com', password_hash=User.encode_password('123456'))
# db.session.add(test_user)
# db.session.commit()
#
# query = db.session.query(User)
# print(query.all())