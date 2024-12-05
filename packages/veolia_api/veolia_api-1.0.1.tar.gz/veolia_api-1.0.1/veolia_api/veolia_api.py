"""Veolia API client"""

import base64
import hashlib
import logging
import os
from http import HTTPStatus
from urllib.parse import parse_qs, urlencode, urlparse

import aiohttp

from veolia_api.exceptions import VeoliaAPIError

from .constants import (
    AUTHORIZE_ENDPOINT,
    AUTHORIZE_RESUME_ENDPOINT,
    BACKEND_ISTEFR,
    BASE_URL,
    CALLBACK_ENDPOINT,
    CLIENT_ID,
    CODE_CHALLENGE_METHODE,
    LOGIN_IDENTIFIER_ENDPOINT,
    LOGIN_PASSWORD_ENDPOINT,
    LOGIN_URL,
    MFA_DETECT_BROWSER_CAPABILITIES_ENDPOINT,
    MFA_WEBAUTHN_PLATFORM_ENROLLMENT_ENDPOINT,
    OAUTH_TOKEN,
    TYPE_FRONT,
    AlertSettings,
    ConsumptionType,
)


class VeoliaAPI:
    """Veolia API client"""

    def __init__(self, username: str, password: str) -> None:
        """Initialize the Veolia API client"""
        self.username = username
        self.password = password
        self.session = aiohttp.ClientSession()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.access_token = None
        self.code = None
        self.verifier = None
        self.id_abonnement = None
        self.numero_pds = None
        self.contact_id = None
        self.tiers_id = None
        self.numero_compteur = None
        self.date_debut_abonnement = None

        self.api_flow = {
            AUTHORIZE_ENDPOINT: {
                "method": "GET",
                "params": self._get_authorize_params,
                "success_status": HTTPStatus.FOUND,
            },
            LOGIN_IDENTIFIER_ENDPOINT: {
                "method": "POST",
                "params": lambda state: {
                    "username": self.username,
                    "js-available": "true",
                    "webauthn-available": "true",
                    "is-brave": "false",
                    "webauthn-platform-available": "true",
                    "action": "default",
                    "state": state,
                },
                "success_status": HTTPStatus.FOUND,
            },
            LOGIN_PASSWORD_ENDPOINT: {
                "method": "POST",
                "params": lambda state: {
                    "username": self.username,
                    "password": self.password,
                    "action": "default",
                    "state": state,
                },
                "success_status": HTTPStatus.FOUND,
            },
            AUTHORIZE_RESUME_ENDPOINT: {
                "method": "GET",
                "params": None,
                "success_status": HTTPStatus.FOUND,
            },
            MFA_DETECT_BROWSER_CAPABILITIES_ENDPOINT: {
                "method": "POST",
                "params": lambda state: {
                    "js-available": "true",
                    "webauthn-available": "true",
                    "is-brave": "false",
                    "webauthn-platform-available": "true",
                    "action": "default",
                    "state": state,
                },
                "success_status": HTTPStatus.FOUND,
            },
            MFA_WEBAUTHN_PLATFORM_ENROLLMENT_ENDPOINT: {
                "method": "POST",
                "params": lambda state: {
                    "action": "refuse-add-device",
                    "state": state,
                },
                "success_status": HTTPStatus.FOUND,
            },
            CALLBACK_ENDPOINT: {
                "method": "GET",
                "params": lambda state: {
                    "code": self.code,
                    "state": state,
                },
                "success_status": HTTPStatus.OK,
            },
        }

    @staticmethod
    def _base64_url_encode(data: bytes) -> str:
        """Base64 URL encode the data"""
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

    @staticmethod
    def _sha256(data: bytes) -> bytes:
        """Calculate the SHA-256 hash of the data"""
        return hashlib.sha256(data).digest()

    def _get_authorize_params(self, state: str | None) -> dict:
        """Get the parameters for the /authorize API call"""
        state = self._base64_url_encode(os.urandom(32))
        nonce = self._base64_url_encode(os.urandom(32))
        verifier = self._base64_url_encode(os.urandom(32))
        challenge = self._base64_url_encode(self._sha256(verifier.encode("utf-8")))
        self.verifier = verifier
        return {
            "audience": BACKEND_ISTEFR,
            "redirect_uri": f"{BASE_URL}{CALLBACK_ENDPOINT}",
            "client_id": CLIENT_ID,
            "scope": "openid profile email offline_access",
            "response_type": "code",
            "state": state,
            "nonce": nonce,
            "response_mode": "query",
            "code_challenge": challenge,
            "code_challenge_method": CODE_CHALLENGE_METHODE,
            "auth0Client": self._base64_url_encode(
                b'{"name": "auth0-react", "version": "1.11.0"}',
            ),
        }

    async def make_request(
        self,
        url: str,
        method: str,
        params: dict | None = None,
    ) -> aiohttp.ClientResponse:
        """Make an HTTP request"""
        self.logger.info("Making %s request to %s with params: %s", method, url, params)
        headers = {}

        if method == "GET":
            async with self.session.get(
                url,
                headers=headers,
                params=params,
                allow_redirects=False,
            ) as response:
                self.logger.info(
                    "Received response with status code %s",
                    response.status,
                )
                return response
        elif method == "POST":
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            headers["Cache-Control"] = "no-cache"
            async with self.session.post(
                url,
                headers=headers,
                data=urlencode(params),
                allow_redirects=False,
            ) as response:
                self.logger.info(
                    "Received response with status code %s",
                    response.status,
                )
                return response
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

    async def execute_flow(self) -> None:
        """Execute the login flow"""
        next_url = "/authorize"
        state = None

        while next_url:
            config = self.api_flow[next_url]
            full_url = (
                f"{LOGIN_URL}{next_url}"
                if next_url != CALLBACK_ENDPOINT
                else f"{BASE_URL}{next_url}"
            )

            params = config["params"](state) if config["params"] else {}

            if state:
                full_url = f"{full_url}?state={state}"

            response = await self.make_request(full_url, config["method"], params)

            if (
                response.status == HTTPStatus.BAD_REQUEST
                and next_url == LOGIN_PASSWORD_ENDPOINT
            ):
                raise VeoliaAPIError("Invalid username or password")
            if response.status != config["success_status"]:
                raise VeoliaAPIError(
                    f"API call to {full_url} failed with status {response.status}",
                )

            if response.status == HTTPStatus.FOUND:
                redirect_url = urlparse(response.headers.get("Location"))
                next_url = redirect_url.path
                new_state = parse_qs(redirect_url.query).get("state")
                if new_state:
                    state = new_state[0]

                if next_url == CALLBACK_ENDPOINT:
                    self.code = parse_qs(redirect_url.query).get("code", [None])[0]
                    if not self.code:
                        raise VeoliaAPIError("Authorization code not found")
                    self.logger.info("Authorization code received")
            elif response.status == HTTPStatus.OK and next_url == CALLBACK_ENDPOINT:
                next_url = None
            else:
                raise VeoliaAPIError(f"Unexpected 200 response from {full_url}")

    async def login(self) -> None:
        """Login to the Veolia API"""
        self.logger.info("Starting login process...")
        await self.execute_flow()
        await self.request_access_token()

    async def request_access_token(self) -> None:
        """Request the access token"""
        token_url = f"{LOGIN_URL}{OAUTH_TOKEN}"
        self.logger.info("Requesting access token...")
        async with self.session.post(
            token_url,
            json={
                "client_id": CLIENT_ID,
                "grant_type": "authorization_code",
                "code_verifier": self.verifier,
                "code": self.code,
                "redirect_uri": f"{BASE_URL}{CALLBACK_ENDPOINT}",
            },
        ) as token_response:

            if token_response.status != HTTPStatus.OK:
                raise VeoliaAPIError("Token API call error")

            token_data = await token_response.json()
            self.access_token = token_data.get("access_token")
            if not self.access_token:
                raise VeoliaAPIError("Access token not found in the token response")

            self.logger.info("Access token received")

            headers = {"Authorization": f"Bearer {self.access_token}"}
            async with self.session.get(
                url=f"{BACKEND_ISTEFR}/espace-client?type-front={TYPE_FRONT}",
                headers=headers,
            ) as userdata_response:
                if userdata_response.status != HTTPStatus.OK:
                    raise VeoliaAPIError("Espace-client call error")

                userdata = await userdata_response.json()
                self.id_abonnement = (
                    userdata.get("contacts", None)[0]
                    .get("tiers", None)[0]
                    .get("abonnements", None)[0]
                    .get("id_abonnement", None)
                )
                self.tiers_id = (
                    userdata.get("contacts", None)[0]
                    .get("tiers", None)[0]
                    .get("id", None)
                )
                self.contact_id = userdata.get("contacts", None)[0].get(
                    "id_contact",
                    None,
                )
                self.numero_compteur = (
                    userdata.get("contacts", None)[0]
                    .get("tiers", None)[0]
                    .get("abonnements", None)[0]
                    .get("numero_compteur", None)
                )
                if (
                    not self.id_abonnement
                    or not self.tiers_id
                    or not self.contact_id
                    or not self.numero_compteur
                ):
                    raise VeoliaAPIError("Some user data not found in the response")

            # Facturation request
            async with self.session.get(
                url=f"{BACKEND_ISTEFR}/abonnements/{self.id_abonnement}/facturation",
                headers=headers,
            ) as facturation_response:
                if facturation_response.status != HTTPStatus.OK:
                    raise VeoliaAPIError("Facturation call error")

                facturation_data = await facturation_response.json()
                self.numero_pds = facturation_data.get("numero_pds")
                if not self.numero_pds:
                    raise VeoliaAPIError("numero_pds not found in the response")

                self.date_debut_abonnement = facturation_data.get(
                    "date_debut_abonnement",
                )
                if not self.date_debut_abonnement:
                    raise VeoliaAPIError(
                        "date_debut_abonnement not found in the response",
                    )

    async def get_consumption_data(
        self,
        data_type: ConsumptionType,
        year: int,
        month: int | None = None,
    ) -> dict:
        """Get the water consumption data"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "annee": year,
            "numero-pds": self.numero_pds,
            "date-debut-abonnement": self.date_debut_abonnement,
        }

        if data_type == ConsumptionType.MONTHLY and month is not None:
            params["mois"] = month
            endpoint = "journalieres"
        elif data_type == ConsumptionType.YEARLY:
            endpoint = "mensuelles"
        else:
            raise ValueError("Invalid data type or missing month for monthly data")

        url = f"{BACKEND_ISTEFR}/consommations/{self.id_abonnement}/{endpoint}"

        async with self.session.get(url, headers=headers, params=params) as response:
            self.logger.info("Received response with status code %s", response.status)
            if response.status != HTTPStatus.OK:
                raise VeoliaAPIError("Get data call error")
            return await response.json()

    async def get_alerts(self) -> dict:
        """Get the consumption alerts"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "abo_id": self.id_abonnement,
        }
        url = f"{BACKEND_ISTEFR}/alertes/{self.numero_pds}"

        async with self.session.get(url, headers=headers, params=params) as response:
            self.logger.info("Received response with status code %s", response.status)
            if response.status != HTTPStatus.OK:
                raise VeoliaAPIError(
                    f"Get alerts call error status code {response.status}",
                )
            return await response.json()

    async def set_alerts(self, alert_settings: AlertSettings) -> None:
        """Set the consumption alerts"""
        url = f"{BACKEND_ISTEFR}/alertes/{self.numero_pds}"
        payload = {}

        if alert_settings.daily_enabled:
            payload["alerte_journaliere"] = {
                "seuil": alert_settings.daily_threshold,
                "unite": "L",
                "souscrite": True,
                "contact_channel": {
                    "subscribed_by_email": alert_settings.daily_contact_email,
                    "subscribed_by_mobile": alert_settings.daily_contact_sms,
                },
            }

        if alert_settings.monthly_enabled:
            payload["alerte_mensuelle"] = {
                "seuil": alert_settings.monthly_threshold,
                "unite": "M3",
                "souscrite": True,
                "contact_channel": {
                    "subscribed_by_email": alert_settings.monthly_contact_email,
                    "subscribed_by_mobile": alert_settings.monthly_contact_sms,
                },
            }

        payload.update(
            {
                "contact_id": self.contact_id,
                "numero_compteur": self.numero_compteur,
                "tiers_id": self.tiers_id,
                "abo_id": str(self.id_abonnement),
                "type_front": TYPE_FRONT,
            },
        )
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        async with self.session.post(url, headers=headers, json=payload) as response:
            self.logger.info("Received response with status code %s ", response.status)
            if response.status != HTTPStatus.NO_CONTENT:
                raise VeoliaAPIError("Set alerts call error")

    async def close(self) -> None:
        """Close the session"""
        await self.session.close()
