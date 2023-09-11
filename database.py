from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, Boolean, BigInteger, DateTime, Float, Table
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.schema import MetaData
# engine = create_engine('postgresql://postgres:serge2002@127.0.0.1:5432/china_cars')  # local
# engine = create_engine('postgresql://china_car_auction:qxQfkRt3rqTzyJ76oHFy@80.89.239.246:5433/china_car_auction')
db_url = 'postgresql://postgres:serge2002@127.0.0.1:5432/AlibabaParse'
engine = create_engine(db_url, pool_size=100, max_overflow=25, pool_recycle=60, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
metadata = MetaData()

def create_all_tables():
    Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()




# class Car(Base):
#     __tablename__ = 'car'
#     id = Column(Integer, primary_key=True)
#     model = Column(String)
#     xpath = Column(String)
#     year = Column(String)
#     color = Column(String)
#     kpp = Column(String)
#     mileage = Column(String)
#     kuzov = Column(String)
#     eco = Column(String)
#     eng_v = Column(String)
#     lot_date = Column(String)
#     kpp_type = Column(String)
#     horse_power = Column(String)
#     engine_type = Column(String)
#     privod = Column(String)
#     lot_city = Column(String)
#     price = Column(String)
#     status = Column(Boolean)


# def create_car_table(table_name, session):
#     if table_name not in metadata.tables:
#         attr_dict = {
#             '__tablename__': table_name,
#             'id': Column(Integer, primary_key=True),
#             'model': Column(String),
#             'xpath': Column(String),
#             'year': Column(String),
#             'color': Column(String),
#             'kpp': Column(String),
#             'mileage': Column(String),
#             'kuzov': Column(String),
#             'eco': Column(String),
#             'eng_v': Column(String),
#             'lot_date': Column(String),
#             'kpp_type': Column(String),
#             'horse_power': Column(String),
#             'engine_type': Column(String),
#             'privod': Column(String),
#             'lot_city': Column(String),
#             'price': Column(String),
#             'status': Column(Boolean)
#         }
#         Car_models_Class = type(f'Table{table_name}Class', (Base,), attr_dict)
#         return Car_models_Class
#     else:
#         return session.execute(Table(table_name, metadata, autoload_with=engine))
#
#
# def create_car_image_table(table_name, session):
#     if table_name not in metadata.tables:
#         attr_dict__image = {
#             '__tablename__': table_name,
#             'id': Column(Integer, primary_key=True),
#             'car_id': Column(Integer),
#             'image_url': Column(String)
#         }
#         Car_immages_Class = type(f'TableImmage{table_name}Class', (Base,), attr_dict__image)
#         return Car_immages_Class
#     else:
#         return session.execute(Table(table_name, metadata, autoload_with=engine))
def create_car_table(table_name):
    model_class_name = f"Table{table_name}Class"

    if model_class_name in globals():
        return globals()[model_class_name]

    attr_dict = {
        '__tablename__': table_name,
        'id': Column(Integer, primary_key=True),
        'model': Column(String),
        'xpath': Column(String),
        'year': Column(String),
        'color': Column(String),
        'kpp': Column(String),
        'mileage': Column(String),
        'kuzov': Column(String),
        'eco': Column(String),
        'eng_v': Column(String),
        'lot_date': Column(String),
        'kpp_type': Column(String),
        'horse_power': Column(String),
        'engine_type': Column(String),
        'privod': Column(String),
        'lot_city': Column(String),
        'price': Column(String),
        'status': Column(Boolean)
    }

    car_model_class = type(model_class_name, (Base,), attr_dict)
    globals()[model_class_name] = car_model_class
    return car_model_class


def create_car_image_table(table_name):
    image_class_name = f"TableImmage{table_name}Class"

    if image_class_name in globals():
        return globals()[image_class_name]

    attr_dict__image = {
        '__tablename__': table_name,
        'id': Column(Integer, primary_key=True),
        'car_id': Column(Integer),
        'image_url': Column(String)
    }

    car_image_class = type(image_class_name, (Base,), attr_dict__image)
    globals()[image_class_name] = car_image_class
    return car_image_class


