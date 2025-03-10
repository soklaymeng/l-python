import sentry_sdk
import logging
from flask import Flask
from sentry_sdk.integrations.logging import LoggingIntegration

# Configure Sentry Logging Integration
sentry_logging = LoggingIntegration(
    level=logging.DEBUG,  # Capture logs from DEBUG and above
    event_level=logging.ERROR,  # Send ERROR and above to Sentry as events
)

# Initialize Sentry SDK
sentry_sdk.init(
    dsn="https://733a90adbf1ac021a78495ad1e56bf75@o4508914404229120.ingest.us.sentry.io/4508929949696000",
    integrations=[sentry_logging],  # Add logging integration
    send_default_pii=True,
    traces_sample_rate=1.0,  # Adjust based on performance monitoring needs
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Ensure DEBUG logs are recorded locally
logger = logging.getLogger(__name__)  # Get logger instance

app = Flask(__name__)

@app.route("/")
def hello_world():
    # Log messages at different levels
    logger.debug("This is a test debug log")  # Now should appear in Sentry
    logger.info("This is an info log")
    logger.warning("A division by zero is about to occur!")

    try:
        1 / 0  # Raises an error
    except ZeroDivisionError as e:
        logger.error("ZeroDivisionError occurred", exc_info=True)  # Log locally
        sentry_sdk.capture_exception(e)  # Capture in Sentry

    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)  # Explicit host and port
#
#
