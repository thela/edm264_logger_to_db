from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float

from sqlalchemy.orm import relationship, declarative_base

from logger import getgglogger

Base = declarative_base()

logger = getgglogger(__name__)


class FileData(Base):
    __tablename__ = 'file_data'

    id = Column(Integer, primary_key=True)
    filename = Column(String(length=30))
    hash_digest = Column(String(length=64), unique=True)

    edm264_c_tables = relationship("EDM264_C", back_populates="related_file")
    edm264_l_tables = relationship("EDM264_L", back_populates="related_file")
    edm264_dm_tables = relationship("EDM264_dM", back_populates="related_file")
    edm264_m_tables = relationship("EDM264_M", back_populates="related_file")

    def __repr__(self):
        return f"FileData(id={self.id!r}, filename={self.filename!r}, hash_digest={self.hash_digest!r})"


class MetaData(Base):
    __tablename__ = 'data_metadata'

    id = Column(Integer, primary_key=True)

    instrument_model = Column(String(length=30))
    serial = Column(String(length=30))
    location = Column(String(length=30))
    firmware_rev = Column(String(length=30))
    software_rev = Column(String(length=30))

    edm264_c_tables = relationship("EDM264_C", back_populates="metadata_related")
    edm264_l_tables = relationship("EDM264_L", back_populates="metadata_related")
    edm264_dm_tables = relationship("EDM264_dM", back_populates="metadata_related")
    edm264_m_tables = relationship("EDM264_M", back_populates="metadata_related")

    def __repr__(self):
        model_fields = ['id', 'instrument_model', 'serial', 'location', 'firmware_rev', 'software_rev']
        return f"MetaData(id={self.id!r}" + \
            ', '.join([f'{item}={getattr(self, item)!r}' for item in model_fields]) +\
        ")"


class EDM264_C(Base):
    __tablename__ = 'edm264_c'
    grouping = {
        'fine': [
            'um253', 'um298', 'um352', 'um414', 'um488', 'um576', 'um679', 'um800', 'um943', 'um1112', 'um1310',
            'um1545', 'um1821', 'um2146'],
        'coarse': [
            'um2530', 'um2982', 'um3515', 'um4144', 'um4884', 'um5757', 'um6787', 'um8000', 'um9430', 'um11120',
            'um13100', 'um15450', 'um18210', 'um21460', 'um25300', 'um29820', 'um35150']
    }

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    file_data = Column(Integer, ForeignKey('file_data.id'))
    data_metadata = Column(Integer, ForeignKey('data_metadata.id'))

    um253 = Column(Float)
    um298 = Column(Float)
    um352 = Column(Float)
    um414 = Column(Float)
    um488 = Column(Float)
    um576 = Column(Float)
    um679 = Column(Float)
    um800 = Column(Float)
    um943 = Column(Float)
    um1112 = Column(Float)
    um1310 = Column(Float)
    um1545 = Column(Float)
    um1821 = Column(Float)
    um2146 = Column(Float)
    um2530 = Column(Float)
    um2982 = Column(Float)
    um3515 = Column(Float)
    um4144 = Column(Float)
    um4884 = Column(Float)
    um5757 = Column(Float)
    um6787 = Column(Float)
    um8000 = Column(Float)
    um9430 = Column(Float)
    um11120 = Column(Float)
    um13100 = Column(Float)
    um15450 = Column(Float)
    um18210 = Column(Float)
    um21460 = Column(Float)
    um25300 = Column(Float)
    um29820 = Column(Float)
    um35150 = Column(Float)

    related_file = relationship("FileData", back_populates="edm264_c_tables")
    metadata_related = relationship("MetaData", back_populates="edm264_c_tables")

    def __repr__(self):
        return f"EDM264_C(id={self.id!r}, datetime={self.datetime!r})"

    def as_dict(self):
        """
        :return: datetime and the concentration per cm3 of fine and coarse particles
        """
        return {
            'datetime': self.datetime,
            'fine': sum([getattr(self, attr) for attr in self.grouping['fine']])*.001,
            'coarse':  sum([getattr(self, attr) for attr in self.grouping['coarse']])*.001,
        }


class EDM264_dM(Base):
    __tablename__ = 'edm264_dm'
    grouping = {
        'fine': [
            'um253', 'um298', 'um352', 'um414', 'um488', 'um576', 'um679', 'um800', 'um943', 'um1112', 'um1310',
            'um1545', 'um1821', 'um2146'],
        'coarse': [
            'um2530', 'um2982', 'um3515', 'um4144', 'um4884', 'um5757', 'um6787', 'um8000', 'um9430', 'um11120',
            'um13100', 'um15450', 'um18210', 'um21460', 'um25300', 'um29820', 'um35150']
    }

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    file_data = Column(Integer, ForeignKey('file_data.id'))
    data_metadata = Column(Integer, ForeignKey('data_metadata.id'))

    um253 = Column(Float)
    um298 = Column(Float)
    um352 = Column(Float)
    um414 = Column(Float)
    um488 = Column(Float)
    um576 = Column(Float)
    um679 = Column(Float)
    um800 = Column(Float)
    um943 = Column(Float)
    um1112 = Column(Float)
    um1310 = Column(Float)
    um1545 = Column(Float)
    um1821 = Column(Float)
    um2146 = Column(Float)
    um2530 = Column(Float)
    um2982 = Column(Float)
    um3515 = Column(Float)
    um4144 = Column(Float)
    um4884 = Column(Float)
    um5757 = Column(Float)
    um6787 = Column(Float)
    um8000 = Column(Float)
    um9430 = Column(Float)
    um11120 = Column(Float)
    um13100 = Column(Float)
    um15450 = Column(Float)
    um18210 = Column(Float)
    um21460 = Column(Float)
    um25300 = Column(Float)
    um29820 = Column(Float)
    um35150 = Column(Float)

    related_file = relationship("FileData", back_populates="edm264_dm_tables")
    metadata_related = relationship("MetaData", back_populates="edm264_dm_tables")

    def __repr__(self):
        return f"EDM264_dM(id={self.id!r}, datetime={self.datetime!r})"

    def as_dict(self):
        """
        :return: datetime and the concentration per cm3 of fine and coarse particles
        """
        return {
            'datetime': self.datetime,
            'fine': sum([getattr(self, attr) for attr in self.grouping['fine']])*.001,
            'coarse':  sum([getattr(self, attr) for attr in self.grouping['coarse']])*.001,
        }


class EDM264_L(Base):
    __tablename__ = 'edm264_l'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    file_data = Column(Integer, ForeignKey('file_data.id'))
    data_metadata = Column(Integer, ForeignKey('data_metadata.id'))

    P = Column(String(length=2))
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    hour = Column(Integer)
    minute = Column(Integer)
    second = Column(Integer)
    location = Column(Integer)
    grav_factor = Column(Integer)
    error = Column(Integer)
    battery = Column(Float)
    motor_current = Column(Integer)
    temperature_out = Column(Float)
    humidity_out = Column(Float)
    wind_velocity = Column(Float)
    pressure = Column(Float)
    wind_direction = Column(Float)
    rain = Column(Float)
    IV = Column(Integer)
    P_weight = Column(Float)
    P_vol = Column(Float)
    humidity_i = Column(Float)
    temp_i = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Integer)
    flow = Column(String(length=6))
    sflow = Column(Integer)
    svc_temp_set = Column(Integer)
    svc_temp = Column(Integer)

    related_file = relationship("FileData", back_populates="edm264_l_tables")
    metadata_related = relationship("MetaData", back_populates="edm264_l_tables")

    def __repr__(self):
        return f"EDM264_L(id={self.id!r}, datetime={self.datetime!r})"


class EDM264_M(Base):
    __tablename__ = 'edm264_m'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    file_data = Column(Integer, ForeignKey('file_data.id'))
    data_metadata = Column(Integer, ForeignKey('data_metadata.id'))
    
    tsp = Column(Float)
    pm10 = Column(Float)
    pm4 = Column(Float)
    pm2_5 = Column(Float)
    pm1 = Column(Float)
    pm_coarse = Column(Float)
    inhalable = Column(Float)
    thoracic = Column(Float)
    respirable = Column(Float)
    pm10_iaq = Column(Float)
    pm2_5_iaq = Column(Float)
    pm1_iaq = Column(Float)

    related_file = relationship("FileData", back_populates="edm264_m_tables")
    metadata_related = relationship("MetaData", back_populates="edm264_m_tables")

    # from https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    def as_dict(self):
        columns = ['datetime', 'pm10', 'pm2_5', 'pm1']
        return {c: getattr(self, c) for c in columns}

    def __repr__(self):
        return f"EDM264_L(id={self.id!r}, datetime={self.datetime!r})"
