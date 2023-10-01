from sqlalchemy import Column, Integer, String, Boolean, ARRAY, DateTime, func, Table, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

admins_association_table = Table(
    'company_admins',
    Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

members_association_table = Table(
    'company_members',
    Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_email = Column(String(255), unique=True, nullable=False)
    user_firstname = Column(String(100), nullable=True)
    user_lastname = Column(String(100), nullable=True)
    user_status = Column(String(100), nullable=True)
    user_city = Column(String(50), nullable=True)
    user_phone = Column(String(20), nullable=True)
    user_links = Column(ARRAY(String), nullable=True)
    user_avatar = Column(String, nullable=True)
    password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False)
    company_title = Column(String(100), nullable=True)
    company_description = Column(String, nullable=True)
    company_city = Column(String(50), nullable=True)
    company_phone = Column(String(50), nullable=True)
    company_links = Column(ARRAY(String), nullable=True)
    company_avatar = Column(String, nullable=True)
    is_visible = Column(Boolean, default=True)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', backref='companies')
    admins = relationship('User', secondary=admins_association_table, backref='admins_of_companies')
    members = relationship('User', secondary=members_association_table, backref='member_of_companies')


class UsersCompaniesActions(Base):
    __tablename__ = "users_companies_actions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    action = Column(Enum('request_invitation', 'request_join', name='ActionEnum'))
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    user = relationship('User', backref='users_companies_actions')
    company = relationship('Company', backref='users_companies_actions')

