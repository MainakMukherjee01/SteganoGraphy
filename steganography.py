from stegano import lsb
from PIL import Image


def encode_image(image_path, message):
    """
    This function encodes a message into an image using steganography.

    Parameters:
    image_path (str): The path to the image file to be encoded
    message (str): The message to be encoded

    Returns:
    str: The path to the encoded image file
    """
    try:
        # Open the image file
        image = Image.open(image_path)

        # Encode the message into the image using LSB steganography
        encoded_image = lsb.hide(image, message)

        # Save the encoded image to a new file
        encoded_image_path = "encoded_" + image_path
        encoded_image.save(encoded_image_path)

        return encoded_image_path
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        return None


def decode_image(image_path):
    """
    This function decodes a message from an image using steganography.

    Parameters:
    image_path (str): The path to the image file to be decoded

    Returns:
    str: The decoded message
    """
    try:
        # Open the image file
        encoded_image = Image.open(image_path)

        # Decode the message from the image using LSB steganography
        decoded_message = lsb.reveal(encoded_image)

        return decoded_message
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        return None


def menu():
    """
    This function displays a menu of options for encoding and decoding images using steganography.
    """
    while True:
        print("Select an option:")
        print("1. Encode image")
        print("2. Decode image")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            image_path = input("Enter the path to the image file: ")
            message = input("Enter the message to be encoded: ")
            encoded_image_path = encode_image(image_path, message)
            if encoded_image_path:
                print(f"Encoded image saved to {encoded_image_path}")
        elif choice == "2":
            image_path = input("Enter the path to the image file: ")
            decoded_message = decode_image(image_path)
            if decoded_message:
                print(f"Decoded message: {decoded_message}")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
menu()