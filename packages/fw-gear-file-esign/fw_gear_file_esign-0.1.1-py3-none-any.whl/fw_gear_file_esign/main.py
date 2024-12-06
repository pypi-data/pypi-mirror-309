import sys
import os
import hashlib
import logging
from fw_gear_file_esign.utils import (
    check_mfa_verification,
    sign_file_with_user_id,
)
from typing import Tuple
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import unicodedata

log = logging.getLogger(__name__)


class SignatureVerificationError(Exception):
    """Custom exception for signature verification failures."""

    pass


def verify_file_signature(
    file_path: str, public_key: RSAPublicKey
) -> Tuple[str, str, str]:
    """Verify the signature of a text file embedded with zero-width characters.

    Args:
        file_path (str): Path to the signed file.
        public_key (RSAPublicKey): RSA public key used for verification.

    Returns:
        Tuple[str, str, str]: A tuple containing the user ID, timestamp, and signature purpose if verification succeeds.

    Raises:
        SignatureVerificationError: If the verification process fails.
    """

    try:
        # Read the file content
        with open(file_path, "r", encoding="utf-8", errors="strict") as f:
            content = f.read()

        # Normalize the content to NFC form to ensure consistent encoding of zero-width characters
        content = unicodedata.normalize("NFC", content)
        log.debug(f"Content: {content}")
        log.debug(f"Content length:  {len(content)}")

        # Extract the hidden signature
        zero_width_chars = "".join(
            c for c in content if c in {"\u200b", "\u200c", "\u200d"}
        )

        if "\u200d" not in zero_width_chars:
            log.error("Signature separator not found in the file.")
            log.debug(f"len of zero_width_chars: {len(zero_width_chars)}")
            raise SignatureVerificationError("Signature separator not found.")

        # Split the payload and signature
        payload_encoded, signature_encoded = zero_width_chars.split("\u200d")

        # Map zero-width characters back to bits
        reverse_mapping = {"\u200b": "0", "\u200c": "1"}

        # Decode payload
        payload_bits = "".join(reverse_mapping.get(c, "") for c in payload_encoded)
        payload_bytes = [
            payload_bits[i : i + 8] for i in range(0, len(payload_bits), 8)
        ]

        # Validate payload bytes
        if not all(len(b) == 8 and set(b) <= {"0", "1"} for b in payload_bytes):
            log.error("Invalid payload encoding.")
            raise SignatureVerificationError("Invalid payload encoding.")

        signature_payload = "".join(chr(int(b, 2)) for b in payload_bytes)

        try:
            user_id, timestamp, file_id, signature_purpose = signature_payload.split(
                "|"
            )
        except ValueError:
            log.error("Invalid signature payload format.")
            raise SignatureVerificationError("Invalid signature payload format.")

        # Decode signature
        signature_bits = "".join(reverse_mapping.get(c, "") for c in signature_encoded)
        signature_bytes = [
            int(signature_bits[i : i + 8], 2) for i in range(0, len(signature_bits), 8)
        ]
        signature = bytes(signature_bytes)

        # Remove hidden signature from content
        content_without_signature = content.replace(
            payload_encoded + "\u200d" + signature_encoded, ""
        )

        # Compute the file hash
        file_hash = hashlib.sha256(content_without_signature.encode("utf-8")).digest()

        # Recreate data to verify
        data_to_verify = (
            file_hash
            + user_id.encode("utf-8")
            + timestamp.encode("utf-8")
            + file_id.encode("utf-8")
            + signature_purpose.encode("utf-8")
        )

        # Verify the signature
        try:
            public_key.verify(
                signature,
                data_to_verify,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
        except InvalidSignature:
            log.error("Invalid signature detected.")
            raise SignatureVerificationError("Invalid signature detected.")

        # Log the successful verification
        log.info(
            f"Signature verification successful for file '{file_path}'. "
            f"User ID: {user_id}, Timestamp: {timestamp}, Purpose: {signature_purpose}."
        )

        return user_id, timestamp, signature_purpose

    except SignatureVerificationError:
        raise
    except Exception as e:
        log.error(f"Signature verification failed for file '{file_path}': {e}")
        raise SignatureVerificationError(f"Verification failed: {e}") from e


def run(
    code: str,
    email: str,
    file_path: str,
    out_file_path: str,
    private_key: RSAPrivateKey,
    signature_purpose: str,
) -> None:
    """Runs the file signing process after verifying MFA.

    Args:
        code (str): MFA code for verification.
        email (str): User's email for MFA verification.
        file_path (str): Path to the file to be signed.
        out_file_path (str): Output path for the signed file.
        private_key (RSAPrivateKey): RSA private key used for signing.
        signature_purpose (str): Purpose of the signature.

    Raises:
        PermissionError: If MFA verification fails.
        Exception: If an unexpected error occurs during signing.
    """
    try:
        log.info("Verifying MFA for the provided user.")
        check_mfa_verification(code, email)
        log.info("MFA verification successful.")

        if not os.path.isfile(file_path):
            log.error("File not found: %s", file_path)
            sys.exit(1)

        log.info("Initiating file signing process.")
        sign_file_with_user_id(
            file_path, out_file_path, email, private_key, signature_purpose
        )
        log.info("File successfully signed.")

    except PermissionError:
        log.error("MFA verification failed.")
        sys.exit(1)

    except Exception as e:
        log.error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)
