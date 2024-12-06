# verify_file.py

import sys
import os
from fw_gear_file_esign.main import verify_file_signature
from datetime import datetime, timezone
from cryptography.hazmat.primitives import serialization


def main():
    if len(sys.argv) != 3:
        print("Usage: python verify_file.py <file_path> <public_key_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    public_key_path = sys.argv[2]

    if not os.path.isfile(file_path):
        print("File not found:", file_path)
        sys.exit(1)

    if not os.path.isfile(public_key_path):
        print("Public key file not found:", public_key_path)
        sys.exit(1)

    # Load the master public key
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )

    result = verify_file_signature(file_path, public_key)
    if result:
        user_id, timestamp = result
        # Convert timestamp to a human-readable format
        try:
            # Get the local timezone
            local_timezone = datetime.now(timezone.utc).astimezone().tzinfo
            # Convert the timestamp to a timezone-aware datetime object
            dt = datetime.fromtimestamp(int(timestamp), tz=local_timezone)
            # Format the datetime with timezone information
            readable_time = dt.strftime("%Y-%m-%d %H:%M:%S %Z")
        except ValueError:
            readable_time = "Invalid timestamp"

        print(f"The file was signed by user: {user_id} at {readable_time}")
    else:
        print("Signature verification failed.")


if __name__ == "__main__":
    main()
