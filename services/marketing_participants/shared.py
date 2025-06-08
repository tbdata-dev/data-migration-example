from sqlalchemy.orm import Session
from models.marketing_participants import MarketingParticipant

def create_mp(db: Session, mp_data: dict):
    mp = MarketingParticipant(**mp_data)
    db.add(mp)
    db.commit()
    db.refresh(mp)
    return mp
