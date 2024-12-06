"""Veolia API model."""

from dataclasses import dataclass


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


@dataclass
class VeoliaAccountData:
    """Data for the Veolia integration."""

    access_token: str = None
    token_expiration: float = 0
    code: str = None
    verifier: str = None
    id_abonnement: str = None
    numero_pds: str = None
    contact_id: str = None
    tiers_id: str = None
    numero_compteur: str = None
    date_debut_abonnement: str = None
    monthly_consumption: list[dict] = None
    daily_consumption: list[dict] = None
    alert_settings: AlertSettings = None
