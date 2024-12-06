import unittest
import logging

# Importing everything from Aitronos to test if the package setup is correct
try:
    from Aitronos import FreddyApi, MessageRequestPayload, StreamEvent, Message, Aitronos, StreamLine
except ImportError as e:
    raise ImportError(f"Failed to import from Aitronos package: {e}")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class PackageSetupTests(unittest.TestCase):
    """Test suite to validate the setup of the Aitronos package."""

    def test_imports(self):
        """Test if all components of Aitronos package can be imported successfully."""
        try:
            # Attempt to instantiate each major component to ensure imports work
            token = "test_token"

            # Aitronos
            aitronos_instance = Aitronos(token)
            self.assertIsInstance(aitronos_instance, Aitronos)

            # FreddyApi
            freddy_api_instance = FreddyApi(token)
            self.assertIsInstance(freddy_api_instance, FreddyApi)

            # Message
            message = Message(content="Hello", role="user")
            self.assertIsInstance(message, Message)

            # MessageRequestPayload
            payload = MessageRequestPayload(
                organization_id=1,
                assistant_id=1,
                messages=[message]
            )
            self.assertIsInstance(payload, MessageRequestPayload)

            # StreamEvent
            event = StreamEvent(
                event=StreamEvent.Event.THREAD_RUN_CREATED,
                status=StreamEvent.Status.QUEUED,
                is_response=False,
                response=None,
                thread_id=123
            )
            self.assertIsInstance(event, StreamEvent)

            log.info("All imports and basic initializations are successful.")

        except Exception as e:
            self.fail(f"Package setup test failed: {e}")


if __name__ == "__main__":
    unittest.main()
