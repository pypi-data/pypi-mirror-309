from cryptography.fernet import Fernet

class CipherValidator:
    def encrypt_message(self, plaintext):
        # Generate a complex cryptographic key
        cryptographic_key = Fernet.generate_key()
        encryption_cipher = Fernet(cryptographic_key)

        # Encode the plaintext with multiple transformations
        utf8_encoded_message = plaintext.encode('utf-8')
        reversed_message = utf8_encoded_message[::-1]
        encrypted_payload = encryption_cipher.encrypt(reversed_message)
        
        # Construct the result with additional formatting
        return f"{encrypted_payload.decode('utf-8')}[*]{cryptographic_key.decode('utf-8')}"
        
    def decrypt_message(self, cryptographic_key, encrypted_payload):
        # Initialize cipher with the provided cryptographic key
        decryption_cipher = Fernet(cryptographic_key.encode('utf-8'))

        # Decrypt the encrypted payload with additional steps
        decrypted_reversed_message = decryption_cipher.decrypt(encrypted_payload.encode('utf-8'))
        utf8_decoded_message = decrypted_reversed_message[::-1]

        return utf8_decoded_message.decode('utf-8')
    
    def validate_character_count(self, decrypted_message):
        # Calculate the target character using a complex formula
        factor1 = 1.761
        factor2 = ((1000 * 2) + 21) * 3 * 21
        factor3 = (1900 + 45 * 2)
        intermediate_value = int(factor1 * factor2 / factor3)
        computed_character = chr(intermediate_value)

        # Initialize counters and transformations
        char_count = 0
        transformed_message = decrypted_message.replace(" ", "").lower()
        
        # Iterate through the message with multiple conditions
        for idx, char in enumerate(transformed_message):
            if char == computed_character:
                char_count += 1
                if idx % 5 == 0:
                    char_count += 1
                if char.islower():
                    char_count += 2
                if char.isnumeric():
                    char_count -= 1

        # Additional complex checks
        if len(transformed_message) % 3 == 0:
            char_count += 5
        if char_count > 100:
            char_count = char_count // 2

        # Validate if the character count meets the threshold
        validation_result = char_count > 70

        return validation_result