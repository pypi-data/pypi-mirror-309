"""Constants for the Veolia API."""

from dataclasses import dataclass
from enum import Enum

# URLS
LOGIN_URL = "https://login.eau.veolia.fr"
BASE_URL = "https://www.eau.veolia.fr"
BACKEND_ISTEFR = "https://prd-ael-sirius-backend.istefr.fr"

# AUTH
CLIENT_ID = "tHBtoPOLiI2NSbCzqYz6pydZ1Xil0Bw2"
CODE_CHALLENGE_METHODE = "S256"

# API Flow Endpoints
OAUTH_TOKEN = "/oauth/token"
AUTHORIZE_ENDPOINT = "/authorize"
AUTHORIZE_RESUME_ENDPOINT = "/authorize/resume"
CALLBACK_ENDPOINT = "/callback"

LOGIN_IDENTIFIER_ENDPOINT = "/u/login/identifier"
LOGIN_PASSWORD_ENDPOINT = "/u/login/password"
MFA_DETECT_BROWSER_CAPABILITIES_ENDPOINT = "/u/mfa-detect-browser-capabilities"
MFA_WEBAUTHN_PLATFORM_ENROLLMENT_ENDPOINT = "/u/mfa-webauthn-platform-enrollment"

TYPE_FRONT = "WEB_ORDINATEUR"


class ConsumptionType(Enum):
    """Consumption type."""

    MONTHLY = "monthly"
    YEARLY = "yearly"


@dataclass
class AlertSettings:
    """Alert settings.
    daily_enabled: bool = To enable or disable daily alerts
    daily_threshold: int = Daily threshold in liters (minimum 100)
    daily_contact_email: bool = To enable or disable daily
        alerts by email (Can't be disabled)
    daily_contact_sms: bool = To enable or disable daily alerts by SMS
    monthly_enabled: bool = To enable or disable monthly alerts
    monthly_threshold: int = Monthly threshold in M3 (minimum 1)
    monthly_contact_email: bool = To enable or disable monthly
        alerts by email (Can't be disabled)
    monthly_contact_sms: bool = To enable or disable monthly alerts by SMS
    """

    daily_enabled: bool
    daily_threshold: int
    daily_contact_email: bool
    daily_contact_sms: bool
    monthly_enabled: bool
    monthly_threshold: int
    monthly_contact_email: bool
    monthly_contact_sms: bool
