from sqlalchemy import Column, Integer, String, Float, Text
from .base import Base
from sqlalchemy.orm import relationship

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    priority = Column(Integer, nullable=True) # set to an int for a scale system, but column was blank in the source data so would need to confirm scale or boolean
    website = Column(String, nullable=True)
    aum = Column(Float, nullable=True)
    sectors = Column(Text, nullable=True) # would likely want to normalize this into a separate table in a real-world scenario, have a many-to-many relationship
    company_type = Column(String, nullable=True) # another field we would want to confirm the options for and potentially make an enum
    coverage_person = Column(String, nullable=True) # kept blank due to coverage person being at the contact level, could either have a list of coverage people or separate coverage table
    sample_portfolio_companies = Column(Text, nullable=True) # kept as text for simplicity, but would want to confirm if we need links to actual companies in our database
    comments = Column(Text, nullable=True)
    description = Column(String, nullable=True)
    # I included some additional fields we might want for a company but were not in the source data
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)

    deals = relationship("Deal", back_populates="company")


