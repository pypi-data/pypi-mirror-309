import typing as t
import backoff
import twilio
import twilio.rest
import twilio.base
import twilio.base.exceptions  # noqa: E401


# Define custom exceptions within this module
class TwilioServiceError(Exception):
    """Exception raised when the Twilio service encounters an error (e.g., server error)."""

    pass


class MissingTOTPFactorError(Exception):
    """Exception raised when a TOTP factor is missing for a user."""

    pass


def _convert_exception(fn: t.Callable) -> t.Callable:
    """Decorator to convert Twilio exceptions into custom exceptions."""

    def _call_and_convert(*args: t.Any, **kwargs: t.Any) -> t.Any:
        try:
            return fn(*args, **kwargs)
        except twilio.base.exceptions.TwilioRestException as e:
            if 500 <= e.status <= 599:
                raise TwilioServiceError(e)  # Use renamed exception
            raise

    return _call_and_convert


class TwilioMFAClient:
    def __init__(self, account_sid: str, auth_token: str, service_sid: str) -> None:
        self._client = twilio.rest.Client(account_sid, auth_token)
        self._verify_subclient = self._client.verify.v2.services(service_sid)

    @backoff.on_exception(backoff.expo, TwilioServiceError, max_tries=3)
    @_convert_exception
    def verify_totp_factor(self, user_hash: str, code: str) -> bool:
        """Verify the TOTP code provided by the user."""
        factor = self._get_factor(user_hash)
        if not factor:
            raise MissingTOTPFactorError("Missing TOTP factor for the user")
        res = self._verify_subclient.entities(user_hash).challenges.create(
            factor_sid=factor.sid, auth_payload=code
        )
        return res.status == "approved"

    def _get_factor(
        self, user_hash: str
    ) -> t.Optional["twilio.rest.verify.v2.service.entity.factor.FactorInstance"]:
        """Retrieve the TOTP factor for the given user."""
        try:
            factors = self._verify_subclient.entities(user_hash).factors.list(limit=1)
        except twilio.base.exceptions.TwilioException as e:
            if "HTTP 404" in str(e):
                return None
            raise
        return factors[0] if factors else None
