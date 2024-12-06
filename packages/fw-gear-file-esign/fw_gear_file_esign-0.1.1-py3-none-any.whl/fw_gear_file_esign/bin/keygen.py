import argparse
import logging
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def setup_logger():
    """Set up the logger for the script."""
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
    )


def generate_master_key_pair(private_key_path: str, public_key_path: str):
    """Generate an RSA master key pair and save them to specified files."""
    try:
        logging.info("Starting the key generation process.")

        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
        )
        logging.info("Private key generated.")

        # Write private key to file
        with open(private_key_path, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
        logging.info(f"Private key saved to {private_key_path}.")

        # Generate public key
        public_key = private_key.public_key()
        logging.info("Public key derived from the private key.")

        # Write public key to file
        with open(public_key_path, "wb") as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )
        logging.info(f"Public key saved to {public_key_path}.")

    except Exception as e:
        logging.error(f"An error occurred during key generation: {e}")
        raise


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Generate an RSA master key pair and save them to specified files."
    )
    parser.add_argument(
        "private_key_path",
        type=str,
        help="Path to save the private key (e.g., master_private_key.pem).",
    )
    parser.add_argument(
        "public_key_path",
        type=str,
        help="Path to save the public key (e.g., master_public_key.pem).",
    )
    args = parser.parse_args()

    # Set up logging
    setup_logger()

    # Check if the files already exist
    if os.path.exists(args.private_key_path):
        logging.warning(
            f"The private key file '{args.private_key_path}' already exists and will be overwritten."
        )
    if os.path.exists(args.public_key_path):
        logging.warning(
            f"The public key file '{args.public_key_path}' already exists and will be overwritten."
        )

    # Generate master key pair
    generate_master_key_pair(args.private_key_path, args.public_key_path)

    logging.info("Master key pair generation completed successfully.")


if __name__ == "__main__":
    main()
