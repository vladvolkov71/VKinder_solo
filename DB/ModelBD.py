import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    vk_id = sa.Column(sa.BigInteger, primary_key=True)
    name = sa.Column(sa.VARCHAR(128), nullable=False)
    surname = sa.Column(sa.VARCHAR(128))
    city = sa.Column(sa.VARCHAR(128))
    sex = sa.Column(sa.Integer)
    age = sa.Column(sa.Integer)
    date_create = sa.Column(sa.TIMESTAMP, server_default=sa.func.now())
    foto_a_1 = sa.Column(sa.VARCHAR(256))
    foto_a_2 = sa.Column(sa.VARCHAR(256))
    foto_a_3 = sa.Column(sa.VARCHAR(256))
    foto_fr_1 = sa.Column(sa.VARCHAR(256))
    foto_fr_2 = sa.Column(sa.VARCHAR(256))
    foto_fr_3 = sa.Column(sa.VARCHAR(256))


class Favorite(Base):
    __tablename__ = "users_favorites"
    id = sa.Column(sa.BigInteger, primary_key=True)
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.vk_id"), nullable=False)
    user_fav_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.vk_id"), nullable=False)
    # favorite = relationship("User", backref="favorite")


class BlackList(Base):
    __tablename__ = "black_list"
    id = sa.Column(sa.BigInteger, primary_key=True)
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.vk_id"), nullable=False)
    user_black_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.vk_id"), nullable=False)
    # black_list = relationship("User", backref="black_list")


def create_tables(engine):
    # Не забыть удалить перед сдачей проекта!!!!!!!!!
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

