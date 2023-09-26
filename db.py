from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

PG_USER = "postgres"
PG_PASSWORD = "111"
PG_DB = "asyncio_hw_db"
PG_HOST = "127.0.0.1"
PG_PORT = 5400
PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

Base = declarative_base()
engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Character(Base):
    # species, starships, vehicles, films - строка с названиями фильмов через запятую? по заданию
    __tablename__ = "character_table"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    home_world = Column(String)
    mass = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)


async def begin_s():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)


async def end_s():
    await engine.dispose()


def get_session():
    return Session()
