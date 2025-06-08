from sqlalchemy import Column, Integer, String, Float, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    title = Column(String, nullable=True)
    group = Column(String, nullable=True) # would want to confirm options and likely make an enum
    sub_vertical = Column(String, nullable=True) # would want to confirm options and likely make an enum
    email = Column(String, nullable=True) # used email to match contacts if email was provided, but some contacts had multiple emails so not a perfect unique identifier.
        # we would want to confirm if users can have multiple emails in our system under one contact or if we need to create separate contacts for each email to track separately
    phone = Column(String, nullable=True)
    secondary_phone = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    coverage_person = Column(String, nullable=True) # kept as a string for simplicity, unsure if internal coverage person would be a user in our system
    preferred_contact_method = Column(String, nullable=True)
    tier = Column(Integer, nullable=True) # assume tier is an integer from the source data, would want to confirm and create enum if not

    marketing_participants = relationship("MarketingParticipant", back_populates="contact")
