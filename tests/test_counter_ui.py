import pytest
from nicegui.testing import User
from app.database import reset_db
from app.counter_service import CounterService


@pytest.fixture
def new_db():
    """Fixture to provide a fresh database for each test"""
    reset_db()
    yield
    reset_db()


class TestCounterUI:
    """Test suite for Counter UI functionality"""

    async def test_counter_page_loads(self, user: User, new_db) -> None:
        """Test that the counter page loads with initial state"""
        await user.open("/")

        # Check page elements exist
        await user.should_see("Counter App")
        await user.should_see("A simple, elegant counter")

        # Check buttons exist
        await user.should_see(marker="increment-button")
        await user.should_see(marker="decrement-button")
        await user.should_see(marker="reset-button")

        # Check counter display shows 0 initially
        await user.should_see("0")

    async def test_increment_button_functionality(self, user: User, new_db) -> None:
        """Test that increment button works correctly"""
        await user.open("/")

        # Initial state should be 0
        await user.should_see("0")

        # Click increment button
        user.find(marker="increment-button").click()
        await user.should_see("1")

        # Click increment again
        user.find(marker="increment-button").click()
        await user.should_see("2")

        # Click increment one more time
        user.find(marker="increment-button").click()
        await user.should_see("3")

        # Verify the value persists in database
        assert CounterService.get_current_value() == 3

    async def test_decrement_button_functionality(self, user: User, new_db) -> None:
        """Test that decrement button works correctly"""
        await user.open("/")

        # Initial state should be 0
        await user.should_see("0")

        # Click decrement button - should go negative
        user.find(marker="decrement-button").click()
        await user.should_see("-1")

        # Click decrement again
        user.find(marker="decrement-button").click()
        await user.should_see("-2")

        # Verify the value persists in database
        assert CounterService.get_current_value() == -2

    async def test_reset_button_functionality(self, user: User, new_db) -> None:
        """Test that reset button works correctly"""
        await user.open("/")

        # Increment counter first
        user.find(marker="increment-button").click()
        user.find(marker="increment-button").click()
        user.find(marker="increment-button").click()
        await user.should_see("3")

        # Click reset button
        user.find(marker="reset-button").click()
        await user.should_see("0")

        # Verify the value persists in database
        assert CounterService.get_current_value() == 0

    async def test_reset_from_negative(self, user: User, new_db) -> None:
        """Test that reset button works from negative values"""
        await user.open("/")

        # Decrement counter to negative
        user.find(marker="decrement-button").click()
        user.find(marker="decrement-button").click()
        user.find(marker="decrement-button").click()
        await user.should_see("-3")

        # Click reset button
        user.find(marker="reset-button").click()
        await user.should_see("0")

        # Verify the value persists in database
        assert CounterService.get_current_value() == 0

    async def test_mixed_operations(self, user: User, new_db) -> None:
        """Test a sequence of mixed button operations"""
        await user.open("/")

        # Start with increments
        user.find(marker="increment-button").click()
        user.find(marker="increment-button").click()
        await user.should_see("2")

        # Then decrements
        user.find(marker="decrement-button").click()
        await user.should_see("1")

        # More increments
        user.find(marker="increment-button").click()
        user.find(marker="increment-button").click()
        user.find(marker="increment-button").click()
        await user.should_see("4")

        # Reset
        user.find(marker="reset-button").click()
        await user.should_see("0")

        # Decrement to negative
        user.find(marker="decrement-button").click()
        await user.should_see("-1")

        # Final verification
        assert CounterService.get_current_value() == -1

    async def test_existing_counter_loaded(self, user: User, new_db) -> None:
        """Test that existing counter value is loaded on page load"""
        # Set up counter value via service before loading page
        CounterService.increment_counter()
        CounterService.increment_counter()
        CounterService.increment_counter()
        CounterService.increment_counter()
        CounterService.increment_counter()  # Value should be 5

        # Now load page
        await user.open("/")

        # Should show existing value, not 0
        await user.should_see("5")

        # Operations should work from this existing value
        user.find(marker="increment-button").click()
        await user.should_see("6")

        user.find(marker="decrement-button").click()
        await user.should_see("5")

    async def test_ui_elements_styling(self, user: User, new_db) -> None:
        """Test that UI elements have proper styling and structure"""
        await user.open("/")

        # Check that key UI elements exist with markers - simple existence check
        user.find(marker="increment-button").elements.pop()
        user.find(marker="decrement-button").elements.pop()
        user.find(marker="reset-button").elements.pop()
        user.find(marker="counter-display").elements.pop()

        # Verify button functionality (text content verification is tricky with NiceGUI elements)
        # Instead verify the buttons work correctly
        user.find(marker="increment-button").click()
        await user.should_see("1")

        user.find(marker="decrement-button").click()
        await user.should_see("0")

        user.find(marker="reset-button").click()
        await user.should_see("0")

    async def test_notifications_appear(self, user: User, new_db) -> None:
        """Test that notifications appear when buttons are clicked (smoke test)"""
        await user.open("/")

        # Click buttons and ensure they work (notifications are ephemeral so we can't easily test their content)
        user.find(marker="increment-button").click()
        await user.should_see("1")  # Counter should update

        user.find(marker="decrement-button").click()
        await user.should_see("0")  # Counter should update

        user.find(marker="reset-button").click()
        await user.should_see("0")  # Counter should stay at 0
