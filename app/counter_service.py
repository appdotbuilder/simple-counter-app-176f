from sqlmodel import Session, select
from app.database import ENGINE
from app.models import Counter
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CounterService:
    """Service class to handle counter operations"""

    @staticmethod
    def get_or_create_counter() -> Counter:
        """Get the current counter or create a new one if none exists"""
        with Session(ENGINE) as session:
            counter = session.exec(select(Counter)).first()
            if counter is None:
                counter = Counter(value=0)
                session.add(counter)
                session.commit()
                session.refresh(counter)
            return counter

    @staticmethod
    def increment_counter() -> int:
        """Increment the counter by 1 and return new value"""
        with Session(ENGINE) as session:
            counter = session.exec(select(Counter)).first()
            if counter is None:
                counter = Counter(value=1)
                session.add(counter)
            else:
                counter.value += 1
                counter.updated_at = datetime.utcnow()
            session.commit()
            return counter.value

    @staticmethod
    def decrement_counter() -> int:
        """Decrement the counter by 1 and return new value"""
        with Session(ENGINE) as session:
            counter = session.exec(select(Counter)).first()
            if counter is None:
                counter = Counter(value=-1)
                session.add(counter)
            else:
                counter.value -= 1
                counter.updated_at = datetime.utcnow()
            session.commit()
            return counter.value

    @staticmethod
    def reset_counter() -> int:
        """Reset the counter to 0 and return new value"""
        with Session(ENGINE) as session:
            counter = session.exec(select(Counter)).first()
            if counter is None:
                counter = Counter(value=0)
                session.add(counter)
            else:
                counter.value = 0
                counter.updated_at = datetime.utcnow()
            session.commit()
            return counter.value

    @staticmethod
    def get_current_value() -> int:
        """Get the current counter value"""
        counter = CounterService.get_or_create_counter()
        return counter.value
