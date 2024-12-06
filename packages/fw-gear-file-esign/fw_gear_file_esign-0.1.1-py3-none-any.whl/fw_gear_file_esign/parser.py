# fw_gear_file_esign/parser.py

import os
import logging
import sys
import base64
from pathlib import Path
from typing import Tuple
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives import serialization

log = logging.getLogger(__name__)


def parse_config(
    context,
) -> Tuple[str, str, str, str, RSAPrivateKey, RSAPublicKey, bool, str]:
    """Parse the gear configuration and extract necessary arguments.

    Args:
        context (GearToolkitContext): The gear toolkit context object.

    Returns:
        Tuple[str, str, str, str, RSAPrivateKey, RSAPublicKey, bool, str]: A tuple containing the MFA code, email,
        file path, output file path, private key, public key, verification flag, and signature purpose.

    Raises:
        ValueError: If required configuration values are missing.
        Exception: For other unexpected errors during configuration parsing.
    """

    # Extract the MFA code from the gear configuration
    code = context.config.get("code")
    if not code:
        raise ValueError("MFA code is required in the gear configuration.")

    # Extract the email (user_id) from the job context using the Flywheel SDK
    fw_client = context.client

    job = fw_client.get_job(context.config_json.get("job", {}).get("id", {}))

    if "origin" in job and "id" in job["origin"]:
        user_id = job["origin"]["id"]
        user = fw_client.get_user(user_id)
        email = user.email
    else:
        raise ValueError("Unable to extract user email from the job context.")

    # Extract the file path from the gear inputs
    file_path = context.get_input_path("input-file")

    # Extract the file name from the file path
    file_stem = Path(file_path).stem  # Get the base file name without extension
    file_suffix = Path(file_path).suffix

    # Construct the new file path
    out_file_path = context.output_dir / f"{file_stem}_signed{file_suffix}"

    # Extract the encoded private key from an environment variable
    encoded_private_key = os.environ.get("ESIGN_SECRET")
    if not encoded_private_key:
        raise ValueError(
            "This gear requires that an private key is passed as an environment variable. Please refer to gear README.md for details."
        )

    # Extract the encoded public key from an environment variable
    encoded_public_key = os.environ.get("ESIGN_PUB")
    if not encoded_public_key:
        raise ValueError(
            "This gear requires that an public key is passed as an environment variable. Please refer to gear README.md for details."
        )

    # Decode Private Key
    try:
        log.info("Decoding the private key.")
        decoded_private_key = base64.b64decode(encoded_private_key.encode("utf-8"))
        private_key = serialization.load_pem_private_key(
            decoded_private_key,
            password=None,
        )
        log.info("Private key successfully loaded into memory.")
    except Exception:
        log.error(
            "Failed to process the private key. Please verify its integrity and ensure it is a valid PEM-encoded key."
        )
        sys.exit(1)

    # Decode Public Key
    try:
        log.info("Decoding the public key.")
        decoded_public_key = base64.b64decode(encoded_public_key.encode("utf-8"))
        public_key = serialization.load_pem_public_key(decoded_public_key)
        log.info("Public key successfully loaded into memory.")
    except Exception as e:
        log.error(f"Failed to process the public key. {e}")
        sys.exit(1)

    # Extract the signature purpose from the gear configuration
    signature_purpose = context.config.get("signature_purpose", "")

    verify = context.config.get("verify", False)

    # Log the parsed arguments (excluding sensitive information)
    log.info(
        f" Detected User={email}, file path={file_path}, signature_purpose={signature_purpose}"
    )

    return (
        code,
        email,
        file_path,
        out_file_path,
        private_key,
        public_key,
        verify,
        signature_purpose,
    )
