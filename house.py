from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String

class House(Base):

	__tablename__ = "house"

	id = Column(Integer, primary_key=True)
	address = Column(String)
	size = Column(String)
	prize = Column(String)
	rooms = Column(String)
	room_configuration = Column(String)
	url = Column(String)

	
	def __init__(self, address, size, prize, rooms, room_configuration, url):
		self.address = address
		self.size = size
		self.prize = prize
		self.rooms = rooms
		self.room_configuration = room_configuration
		self.url = url

	def __repr__(self):
		return "<House('%s', '%s', '%s', '%s', '%s', '%s',)>" % (self.address, self.size, self.prize, self.rooms, self.room_configuration, self.url)