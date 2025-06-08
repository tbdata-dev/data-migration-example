from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class MarketingParticipant(Base):
    __tablename__ = 'marketing_participants'

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=True)
    event_name = Column(String, nullable=True) # pulled from sheet name in source data, would want to confirm if we want to track events in a separate table to include more details such as date, location, etc.
    status = Column(String, nullable=True) # would want to confirm options and likely make an enum

    contact = relationship("Contact", back_populates="marketing_participants")
