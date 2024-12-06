# utils.py

import os
import hashlib
import time
from typing import NamedTuple
import logging

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from fw_gear_file_esign.mfa_client import TwilioMFAClient

log = logging.getLogger(__name__)

# Define a namedtuple to store Twilio credentials
TwilioCreds = NamedTuple(
    "TwilioCreds", [("account_sid", str), ("auth_token", str), ("service_sid", str)]
)


def _get_twilio_creds() -> TwilioCreds:
    """Retrieve Twilio credentials from environment variables.

    Returns:
        TwilioCreds: Named tuple containing the account SID, auth token,
        and service SID for Twilio.

    Raises:
        EnvironmentError: If any required Twilio environment variables are missing.
    """
    # Use uppercase keys for environment variables
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    service_sid = os.environ.get("TWILIO_SERVICE_SID")

    # Return the credentials as a namedtuple
    return TwilioCreds(account_sid, auth_token, service_sid)


def _twilio_user_hash(user_id: str) -> str:
    """Generate a SHA256 hash of the user's ID.

    Args:
        user_id (str): Unique identifier for the user.

    Returns:
        str: SHA256 hash of the user ID.

    Raises:
        ValueError: If the user ID is None or empty.
    """
    if not user_id:
        raise ValueError("User ID cannot be None or empty")
    return hashlib.sha256(user_id.encode("utf-8")).hexdigest()


def get_mfa_client() -> TwilioMFAClient:
    """Instantiate the Twilio MFA client with credentials.

    Returns:
        TwilioMFAClient: Instance of the Twilio MFA client configured with credentials.

    Raises:
        ValueError: If Twilio MFA credentials are missing.
    """
    creds = _get_twilio_creds()
    if not all([creds.account_sid, creds.auth_token, creds.service_sid]):
        raise ValueError("Twilio MFA credentials are missing")

    # Pass the credentials to the TwilioMFAClient
    return TwilioMFAClient(
        creds.account_sid,
        creds.auth_token,
        creds.service_sid,
    )


def check_mfa_verification(code: str, user_id: str) -> None:
    """Verify the MFA code provided by the user.

    Args:
        code (str): MFA code for verification.
        user_id (str): Unique identifier for the user.

    Raises:
        PermissionError: If the MFA verification is unsuccessful.
    """
    mfa_client = get_mfa_client()
    user_hash = _twilio_user_hash(user_id)

    # Only TOTP verification is supported
    if not mfa_client.verify_totp_factor(user_hash, code):
        raise PermissionError("MFA Verification unsuccessful")


def sign_file_with_user_id(
    file_path: str,
    out_file_path: str,
    user_id: str,
    private_key: RSAPrivateKey,
    signature_purpose: str,
) -> None:
    """Sign a file with the user's ID using the appropriate method.

    Args:
        file_path (str): Path to the file to be signed.
        out_file_path (str): Output path for the signed file.
        user_id (str): Unique identifier for the user.
        private_key (RSAPrivateKey): RSA private key used for signing.
        signature_purpose (str): Purpose of the signature.

    Raises:
        IOError: If there is an error in file handling.
        Exception: If signing fails due to an unexpected error.
    """
    # Determine file type
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        sign_pdf_with_user_id(
            file_path, out_file_path, user_id, private_key, signature_purpose
        )
    elif file_extension in [".txt", ".csv", ".md"]:
        sign_text_file_with_user_id(
            file_path, out_file_path, user_id, private_key, signature_purpose
        )
    else:
        sign_binary_file_with_user_id(
            file_path, out_file_path, user_id, private_key, signature_purpose
        )


def sign_text_file_with_user_id(
    file_path: str,
    out_file_path: str,
    user_id: str,
    private_key: RSAPrivateKey,
    signature_purpose: str,
) -> None:
    """Sign a text file by embedding the signature using zero-width characters.

    Args:
        file_path (str): Path to the text file to be signed.
        out_file_path (str): Output path for the signed file.
        user_id (str): Unique identifier for the user.
        private_key (RSAPrivateKey): RSA private key used for signing.
        signature_purpose (str): Purpose of the signature.

    Raises:
        IOError: If there is an error in file handling.
        Exception: If the signing process encounters an unexpected error.
    """
    import uuid

    try:
        # Read the file content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Compute the file hash
        file_hash = hashlib.sha256(content.encode("utf-8")).digest()

        # Get the current timestamp
        timestamp = str(int(time.time()))

        # Generate a unique file ID
        file_id = str(uuid.uuid4())

        # Create data to sign
        data_to_sign = (
            file_hash
            + user_id.encode("utf-8")
            + timestamp.encode("utf-8")
            + file_id.encode("utf-8")
            + signature_purpose.encode("utf-8")
        )

        # Generate the signature using the in-memory private key
        signature = private_key.sign(
            data_to_sign,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        # Convert signature to binary string
        signature_bits = "".join(f"{byte:08b}" for byte in signature)

        # Map bits to zero-width characters
        zero_width_mapping = {"0": "\u200b", "1": "\u200c"}
        encoded_signature = "".join(zero_width_mapping[bit] for bit in signature_bits)

        # Create a signature payload including user_id, timestamp, file_id, and purpose
        signature_payload = f"{user_id}|{timestamp}|{file_id}|{signature_purpose}"

        # Convert signature payload to binary and map to zero-width characters
        payload_bits = "".join(f"{ord(char):08b}" for char in signature_payload)
        encoded_payload = "".join(zero_width_mapping[bit] for bit in payload_bits)

        # Combine encoded payload and signature
        hidden_signature = (
            encoded_payload + "\u200d" + encoded_signature
        )  # Use Zero Width Joiner as a separator

        # Append hidden signature to the content
        content += hidden_signature

        # Write the content back to the file
        with open(out_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        log.info(f"Text file '{out_file_path}' signed successfully.")

    except Exception as e:
        log.error(f"Failed to sign text file '{out_file_path}': {e}")
        raise


def sign_pdf_with_user_id(
    file_path: str,
    out_file_path: str,
    user_id: str,
    private_key: RSAPrivateKey,
    signature_purpose: str,
) -> None:
    """Sign a PDF by embedding the signature in custom metadata.

    Args:
        file_path (str): Path to the PDF file to be signed.
        out_file_path (str): Output path for the signed PDF file.
        user_id (str): Unique identifier for the user.
        private_key (RSAPrivateKey): RSA private key used for signing.
        signature_purpose (str): Purpose of the signature.

    Raises:
        IOError: If file handling fails.
        Exception: If signing fails due to an unexpected error.
    """
    import pikepdf

    try:
        # Read the PDF content and compute hash
        with open(file_path, "rb") as f:
            data = f.read()
        file_hash = hashlib.sha256(data).digest()

        # Get the current timestamp
        timestamp = str(int(time.time()))

        # Create data to sign
        data_to_sign = (
            file_hash
            + user_id.encode("utf-8")
            + timestamp.encode("utf-8")
            + signature_purpose.encode("utf-8")
        )

        # Generate the signature using the in-memory private key
        signature = private_key.sign(
            data_to_sign,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        # Open the PDF and embed the signature in custom metadata
        with pikepdf.open(file_path, allow_overwriting_input=True) as pdf:
            pdf.docinfo["/UserID"] = user_id
            pdf.docinfo["/Timestamp"] = timestamp
            pdf.docinfo["/Purpose"] = signature_purpose
            pdf.docinfo["/Signature"] = signature.hex()

            # Save the signed PDF
            pdf.save(out_file_path)

        log.info(f"PDF file '{out_file_path}' signed successfully.")

    except Exception as e:
        log.error(f"Failed to sign PDF file '{out_file_path}': {e}")
        raise


def sign_binary_file_with_user_id(
    file_path: str,
    out_file_path: str,
    user_id: str,
    private_key: RSAPrivateKey,
    signature_purpose: str,
) -> None:
    """Sign a binary file by creating a signed ZIP archive.

    Args:
        file_path (str): Path to the binary file to be signed.
        out_file_path (str): Output path for the signed ZIP archive.
        user_id (str): Unique identifier for the user.
        private_key (RSAPrivateKey): RSA private key used for signing.
        signature_purpose (str): Purpose of the signature.

    Raises:
        IOError: If file handling fails.
        Exception: If signing fails due to an unexpected error.
    """
    import zipfile

    try:
        # Read the file content
        with open(file_path, "rb") as f:
            data = f.read()

        # Compute the file hash
        file_hash = hashlib.sha256(data).digest()

        # Get the current timestamp
        timestamp = str(int(time.time()))

        # Create data to sign
        data_to_sign = (
            file_hash
            + user_id.encode("utf-8")
            + timestamp.encode("utf-8")
            + signature_purpose.encode("utf-8")
        )

        # Generate the signature using the in-memory private key
        signature = private_key.sign(
            data_to_sign,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        # Prepare the signature info
        signature_info = f"""User ID: {user_id}
Timestamp: {timestamp}
Purpose: {signature_purpose}
Signature: {signature.hex()}"""

        # Create a ZIP archive containing the original file and signature
        zip_filename = out_file_path + ".signed.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            zipf.write(file_path, arcname=os.path.basename(file_path))
            zipf.writestr("signature.txt", signature_info)

        log.info(
            f"Binary file '{file_path}' signed successfully. Signed ZIP saved as '{zip_filename}'."
        )

    except Exception as e:
        log.error(f"Failed to sign binary file '{file_path}': {e}")
        raise
