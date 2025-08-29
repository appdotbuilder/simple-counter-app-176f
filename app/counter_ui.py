from nicegui import ui
from app.counter_service import CounterService
import logging

logger = logging.getLogger(__name__)


class TextStyles:
    """Consistent text styles for the application"""

    HEADING = "text-4xl font-bold text-gray-800 mb-2"
    SUBHEADING = "text-lg text-gray-600 mb-8"
    COUNTER_DISPLAY = "text-8xl font-bold text-blue-600 mb-8 font-mono"


def apply_modern_theme():
    """Apply a modern color scheme"""
    ui.colors(
        primary="#2563eb",  # Professional blue
        secondary="#64748b",  # Subtle gray
        accent="#10b981",  # Success green
        positive="#10b981",
        negative="#ef4444",  # Error red
        warning="#f59e0b",  # Warning amber
        info="#3b82f6",  # Info blue
    )


def create():
    """Create the counter application UI"""

    @ui.page("/")
    def counter_page():
        apply_modern_theme()
        # Page setup with centered layout
        with ui.column().classes("w-full min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100"):
            with ui.column().classes("flex-1 items-center justify-center p-8"):
                # Main card container
                with ui.card().classes(
                    "p-12 bg-white/80 backdrop-blur-sm shadow-2xl rounded-3xl border border-white/30 max-w-md w-full text-center"
                ):
                    # Title
                    ui.label("Counter App").classes(TextStyles.HEADING)
                    ui.label("A simple, elegant counter").classes(TextStyles.SUBHEADING)

                    # Counter display
                    counter_display = ui.label().classes(TextStyles.COUNTER_DISPLAY).mark("counter-display")

                    # Control buttons with modern styling
                    with ui.row().classes("gap-4 justify-center mb-6"):
                        # Decrement button
                        ui.button("-", on_click=lambda: handle_decrement()).classes(
                            "w-14 h-14 text-2xl font-bold bg-red-500 hover:bg-red-600 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-200"
                        ).mark("decrement-button")

                        # Increment button
                        ui.button("+", on_click=lambda: handle_increment()).classes(
                            "w-14 h-14 text-2xl font-bold bg-green-500 hover:bg-green-600 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-200"
                        ).mark("increment-button")

                    # Reset button
                    ui.button("Reset", on_click=lambda: handle_reset()).classes(
                        "px-8 py-3 bg-gray-500 hover:bg-gray-600 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-200 font-semibold"
                    ).mark("reset-button")

        def update_counter_display():
            """Update the counter display with current value"""
            current_value = CounterService.get_current_value()
            counter_display.set_text(str(current_value))

        def handle_increment():
            """Handle increment button click"""
            try:
                new_value = CounterService.increment_counter()
                counter_display.set_text(str(new_value))
                ui.notify(f"Counter incremented to {new_value}", type="positive", position="top")
            except Exception as e:
                logger.error(f"Error incrementing counter: {str(e)}")
                ui.notify(f"Error incrementing counter: {str(e)}", type="negative")

        def handle_decrement():
            """Handle decrement button click"""
            try:
                new_value = CounterService.decrement_counter()
                counter_display.set_text(str(new_value))
                ui.notify(f"Counter decremented to {new_value}", type="info", position="top")
            except Exception as e:
                logger.error(f"Error decrementing counter: {str(e)}")
                ui.notify(f"Error decrementing counter: {str(e)}", type="negative")

        def handle_reset():
            """Handle reset button click"""
            try:
                new_value = CounterService.reset_counter()
                counter_display.set_text(str(new_value))
                ui.notify("Counter reset to 0", type="warning", position="top")
            except Exception as e:
                logger.error(f"Error resetting counter: {str(e)}")
                ui.notify(f"Error resetting counter: {str(e)}", type="negative")

        # Initialize counter display
        update_counter_display()
