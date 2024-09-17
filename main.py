from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker



Base = declarative_base()



# Band model
class Band(Base):
    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hometown = Column(String)
    
    #Relationships
    concerts = relationship('Concert', back_populates='band')

    def __repr__(self):
        return f"Band number: {self.id}"\
                +f"Band Name :{self.name}"\
                +f"Hometown: {self.hometown}"
  
    #Methods
    def band_concerts(self):
        return self.concerts
    
    def band_venues(self):
        return list(set([concert.venue for concert in self.concerts]))

    def play_in_venue(self, venue, date):
        new_concert = Concert(band=self, venue=venue, date=date)
        session.add(new_concert)
        session.commit()

    def all_introductions(self):
        return [concert.introduction() for concert in self.concerts]

    @classmethod
    def most_performances(cls):
        return session.query(cls).join(Concert).group_by(cls.id).order_by(func.count(Concert.id).desc()).first()

# Venue model
class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    city = Column(String)

    #Relationships
    concerts = relationship('Concert', back_populates='venue')
    
    def __repr__(self):
        return f"Venue Number: {self.id}"\
            +f"Venue Name: {self.title}"\
                +f"city: {self.city}" 

    #Methods
    def venue_concerts(self):
        return self.concerts

    def venue_bands(self):
        return list(set([concert.band for concert in self.concerts]))

    def concert_on(self, date):
        return session.query(Concert).filter_by(venue=self, date=date).first()

    def most_frequent_band(self):
        bands=session.query(Band).join(Concert)
        print(bands.filter_by(venue=self).group_by(Band.id).order_by(func.count(Concert.id).desc()).first())

# Concert model
class Concert(Base):
    __tablename__ = 'concerts'

    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey('bands.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    date = Column(String)

    #Relationships
    band = relationship('Band', back_populates='concerts')
    venue = relationship('Venue', back_populates='concerts')
    
    def __repr__(self):
        return f"Concert number;{self.id}"\
            +f"Band id;{self.band_id}"\
                +f"Venue id: {self.venue_id}"\
                +f"date:{self.date}"

    
    #Methods
    def concert_band(self):
        return self.band 

    def concert_venue(self):
        return self.venue

    def hometown_show(self):
        return self.band.hometown == self.venue.city

    def introduction(self):
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"

# Setup database connection
engine = create_engine('sqlite:///concerts.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Linkin_Park = Band(name="Linkin Park ", hometown="Thika")
# KICC = Venue(title="KICC", city="Nairobi")
# TSO = Concert(band=Linkin_Park, venue=KICC, date="2024-09-17")

# session.add_all([Linkin_Park, KICC, TSO])
# session.commit()
