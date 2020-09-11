from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, VARCHAR, DateTime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///users.db',echo=True)
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(255))
    fullname = Column(String)
    password = Column(String)
    age = Column(Integer)

    def __init__(self, name, fullname, password, age):
        self.name = name
        self.fullname = fullname
        self.password = password
        self.age = age


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()
# vasia = Users('vasia','Vasiliy Pupkin','Vasia2000', 19)
# session.add(vasia)
# session.add_all([Users("kolia", "Cool Kolian[S.A.]","kolia$$$", 28),
#                  Users("zina", "Zina Korzina", "zk18", 54)])
for object in session.query(Users).filter(Users.age > 30):
    print(object.fullname, object.password)
session.commit()
# pass
# pass
# pass
# session.commit()
session.close()


