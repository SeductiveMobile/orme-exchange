import db
from sqlalchemy import Column, Integer, String


class User(db.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password_hash = Column(String)

    def __repr__(self):
        return "<User(email='%s', password_hash='%s')>" % (self.email, self.password_hash)


db.Base.metadata.create_all(db.engine)

# test_user = User(email='123@example.com', password_hash='1234654')
# db.session.add(test_user)
# db.session.commit()
