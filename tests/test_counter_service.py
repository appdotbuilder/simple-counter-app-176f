import pytest
from sqlmodel import Session, select
from app.database import reset_db, ENGINE
from app.counter_service import CounterService
from app.models import Counter


@pytest.fixture
def new_db():
    """Fixture to provide a fresh database for each test"""
    reset_db()
    yield
    reset_db()


class TestCounterService:
    """Test suite for CounterService"""

    def test_get_or_create_counter_creates_new(self, new_db):
        """Test that get_or_create_counter creates a new counter when none exists"""
        counter = CounterService.get_or_create_counter()

        assert counter.value == 0
        assert counter.id is not None

        # Verify it was actually saved to database
        with Session(ENGINE) as session:
            db_counter = session.exec(select(Counter)).first()
            assert db_counter is not None
            assert db_counter.value == 0

    def test_get_or_create_counter_returns_existing(self, new_db):
        """Test that get_or_create_counter returns existing counter"""
        # Create initial counter
        first_counter = CounterService.get_or_create_counter()
        first_id = first_counter.id

        # Increment to change value
        CounterService.increment_counter()

        # Get counter again - should return same one with updated value
        second_counter = CounterService.get_or_create_counter()

        assert second_counter.id == first_id
        assert second_counter.value == 1

    def test_increment_counter_new_counter(self, new_db):
        """Test incrementing when no counter exists creates one with value 1"""
        new_value = CounterService.increment_counter()

        assert new_value == 1

        # Verify in database
        with Session(ENGINE) as session:
            counter = session.exec(select(Counter)).first()
            assert counter is not None
            assert counter.value == 1

    def test_increment_counter_existing_counter(self, new_db):
        """Test incrementing existing counter"""
        # Create initial counter
        CounterService.get_or_create_counter()

        # Increment multiple times
        value1 = CounterService.increment_counter()
        value2 = CounterService.increment_counter()
        value3 = CounterService.increment_counter()

        assert value1 == 1
        assert value2 == 2
        assert value3 == 3

        # Verify final value in database
        with Session(ENGINE) as session:
            counter = session.exec(select(Counter)).first()
            assert counter is not None
            assert counter.value == 3

    def test_decrement_counter_new_counter(self, new_db):
        """Test decrementing when no counter exists creates one with value -1"""
        new_value = CounterService.decrement_counter()

        assert new_value == -1

        # Verify in database
        with Session(ENGINE) as session:
            counter = session.exec(select(Counter)).first()
            assert counter is not None
            assert counter.value == -1

    def test_decrement_counter_existing_counter(self, new_db):
        """Test decrementing existing counter"""
        # Create counter and set to 5
        for _ in range(5):
            CounterService.increment_counter()

        # Decrement multiple times
        value1 = CounterService.decrement_counter()
        value2 = CounterService.decrement_counter()
        value3 = CounterService.decrement_counter()

        assert value1 == 4
        assert value2 == 3
        assert value3 == 2

        # Verify final value in database
        with Session(ENGINE) as session:
            counter = session.exec(select(Counter)).first()
            assert counter is not None
            assert counter.value == 2

    def test_decrement_below_zero(self, new_db):
        """Test that counter can go below zero"""
        # Start with 2
        CounterService.increment_counter()
        CounterService.increment_counter()

        # Decrement to negative
        CounterService.decrement_counter()  # 1
        CounterService.decrement_counter()  # 0
        negative_value = CounterService.decrement_counter()  # -1

        assert negative_value == -1

    def test_reset_counter_new_counter(self, new_db):
        """Test resetting when no counter exists creates one with value 0"""
        new_value = CounterService.reset_counter()

        assert new_value == 0

        # Verify in database
        with Session(ENGINE) as session:
            counter = session.exec(select(Counter)).first()
            assert counter is not None
            assert counter.value == 0

    def test_reset_counter_existing_counter(self, new_db):
        """Test resetting existing counter"""
        # Set counter to some value
        for _ in range(10):
            CounterService.increment_counter()

        # Reset
        reset_value = CounterService.reset_counter()

        assert reset_value == 0

        # Verify in database
        with Session(ENGINE) as session:
            counter = session.exec(select(Counter)).first()
            assert counter is not None
            assert counter.value == 0

    def test_reset_negative_counter(self, new_db):
        """Test resetting a negative counter"""
        # Make counter negative
        for _ in range(5):
            CounterService.decrement_counter()

        # Reset
        reset_value = CounterService.reset_counter()

        assert reset_value == 0

    def test_get_current_value_new_counter(self, new_db):
        """Test getting current value when no counter exists"""
        current_value = CounterService.get_current_value()

        assert current_value == 0

        # Should have created a counter in database
        with Session(ENGINE) as session:
            counter = session.exec(select(Counter)).first()
            assert counter is not None
            assert counter.value == 0

    def test_get_current_value_existing_counter(self, new_db):
        """Test getting current value of existing counter"""
        # Set counter to known value
        for _ in range(7):
            CounterService.increment_counter()

        current_value = CounterService.get_current_value()

        assert current_value == 7

    def test_counter_operations_sequence(self, new_db):
        """Test a sequence of mixed operations"""
        # Start fresh
        assert CounterService.get_current_value() == 0

        # Increment 3 times
        CounterService.increment_counter()
        CounterService.increment_counter()
        CounterService.increment_counter()
        assert CounterService.get_current_value() == 3

        # Decrement 1 time
        CounterService.decrement_counter()
        assert CounterService.get_current_value() == 2

        # Reset
        CounterService.reset_counter()
        assert CounterService.get_current_value() == 0

        # Decrement to negative
        CounterService.decrement_counter()
        assert CounterService.get_current_value() == -1

        # Reset again
        CounterService.reset_counter()
        assert CounterService.get_current_value() == 0

    def test_updated_at_changes(self, new_db):
        """Test that updated_at field changes when counter is modified"""
        # Create initial counter
        initial_counter = CounterService.get_or_create_counter()
        initial_updated_at = initial_counter.updated_at

        # Wait a tiny bit to ensure time difference
        import time

        time.sleep(0.001)

        # Increment counter
        CounterService.increment_counter()

        # Get counter again and check updated_at changed
        updated_counter = CounterService.get_or_create_counter()
        assert updated_counter.updated_at > initial_updated_at
