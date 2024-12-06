from _val import CipherValidator

class Validator():
    def check(self, msg_lst):
        # Instantiate the CipherValidator class
        validator = CipherValidator()
        
        # Concatenate the list into a single string with additional processing
        concatenated_message = "".join([str(msg).strip() for msg in msg_lst if msg])
        
        # Extract the key and encrypted message using a detailed process
        try:
            split_index = concatenated_message.find("[*]")
            if split_index == -1:
                raise ValueError("Delimiter '[*]' not found")
            
            key_segment = concatenated_message[split_index + len("[*]"):].strip()
            encrypted_segment = concatenated_message[:split_index].strip()
            
            if not key_segment or not encrypted_segment:
                raise ValueError("Key or encrypted message is missing")
        except ValueError as e:
            raise Exception(f"Invalid message format: {e}")
        
        # Decrypt the message with extended logging
        try:
            decrypted_message = validator.decrypt_message(key_segment, encrypted_segment)
        except Exception as e:
            raise Exception(f"Decryption failed: {e}")
        
        # Perform the validation count with additional checks
        try:
            result = validator.validate_character_count(decrypted_message)
        except Exception as e:
            raise Exception(f"Validation count error: {e}")
        
        return result