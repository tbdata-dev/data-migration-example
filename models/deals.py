from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Deal(Base):
    __tablename__ = 'deals'

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)

    project_name = Column(String, nullable=True)
    date_added = Column(Date, nullable=True)
    sourcing = Column(String, nullable=True)
    transaction_type = Column(String, nullable=True) # would want to confirm options and likely make an enum
    # need to confirm revenue scale (mil, bil, etc.)
    ltm_revenue = Column(Float, nullable=True)
    ltm_ebitda = Column(Float, nullable=True)
    enterprise_value = Column(Float, nullable=True)
    estimated_equity_investment = Column(Float, nullable=True)
    status = Column(String, nullable=True) # would want to confirm options and likely make an enum
    portfolio_company_status = Column(String, nullable=True) # would want to confirm options and likely make an enum
    active_stage = Column(String, nullable=True) # would want to confirm options and likely make an enum
    passed_rationale = Column(String, nullable=True) # would want to confirm options and likely make an enum
    current_owner = Column(String, nullable=True)
    business_description = Column(String, nullable=True)
    lead_md = Column(String, nullable=True) # unsure if we would want to link to a user in our system for this

    # store list of integers as comma-separated string, likely would want to have a separate table to maintain relationships
    banker_contact_ids = Column(String, nullable=True)
    investment_banks = Column(String, nullable=True)

    company = relationship("Company", back_populates="deals")
