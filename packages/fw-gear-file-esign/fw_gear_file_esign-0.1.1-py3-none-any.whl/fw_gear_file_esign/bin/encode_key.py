import argparse
import base64
import logging
import os


def setup_logger():
    """Set up logger for the script."""
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
    )


def encode_pem_to_base64(pem_file_path):
    """Read a PEM file, base64 encode its content, and return the result."""
    try:
        if not os.path.isfile(pem_file_path):
            logging.error(f"The file {pem_file_path} does not exist.")
            return None

        with open(pem_file_path, "rb") as pem_file:
            pem_content = pem_file.read()

        encoded_pem = base64.b64encode(pem_content).decode("utf-8")
        logging.info(f"Successfully encoded the PEM file at {pem_file_path}.")
        return encoded_pem

    except Exception as e:
        logging.error(f"An error occurred while encoding the PEM file: {e}")
        return None


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Base64 encode the contents of a PEM file."
    )
    parser.add_argument(
        "pem_file_path", type=str, help="Path to the PEM file that you want to encode."
    )
    args = parser.parse_args()

    # Set up logging
    setup_logger()

    # Encode the PEM file to Base64
    encoded_pem = encode_pem_to_base64(args.pem_file_path)

    if encoded_pem:
        print(f"Encoded PEM content:\n{encoded_pem}")


if __name__ == "__main__":
    main()
