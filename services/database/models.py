from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

Base = declarative_base()
DATABASE_URL = "sqlite:///services/database/vasuply_data.db"

class Afectados(Base):
    __tablename__ = 'afectados'

    id = Column(Integer, primary_key=True)
    afectado = Column(String(100), nullable=False)
    ubicacion = Column(String(100))
    DNI = Column(String(20), nullable=False)
    telefono = Column(Integer)
    necesidad = Column(Text, nullable=False)
    fecha_registro = Column(String, default=lambda: datetime.datetime.utcnow().isoformat())


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)