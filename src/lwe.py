import numpy as np

class LWE:

    default_n = 256
    default_q = 2**np.ceil(np.log2(default_n*50))

    def keygen(n = default_n, q = default_q):
        """Generate a key pair for the LWE cryptosystem.
        Args:
            n (int): The number of elements in the secret key.
            q (int): The modulus.
        Returns:
            tuple: A tuple containing the secret key and the public key.
        """
        A = np.random.randint(0, q, (n,n)) # Public matrix
        s = np.random.randint(0, q, (n,1)) # Secret key
        e = np.random.normal(0, 1 / np.sqrt(n), (n, 1)).astype(int)  # Gaussian noise
        
        b = np.mod(np.dot(A, s) + e, q) # Public vector
        return (A, b), s
    
    def encrypt_bit(pk, bit, q= default_q):
        """Encrypt a
        Args:
            pk (tuple): The public key.
            bit (int): The bit to encrypt.
            q (int): The modulus.
        Returns:
            tuple: A tuple containing the ciphertext.
        """
        A, b = pk
        
        # Collaspse the whole A matrix into a single row, by randomly picking rows
        # and adding them together.
        rows = np.random.choice(len(A), 3, replace=False)
        a = np.mod(np.sum(A[rows], axis=0), q)
        b = np.mod(np.sum(b[rows], axis=0), q)
        # If the bit is 1, add q/2 to the b vector
        if bit == 1:
            b = np.mod(b + q//2, q)
        else:
            b = np.mod(b, q)
        return (a, b)
    
    def decrypt_bit(sk, ct, q= default_q):
        """Decrypt a ciphertext using the LWE cryptosystem.
        Args:
            sk (np.array): The secret key.
            ct (tuple): The ciphertext to decrypt.
            q (int): The modulus.
        Returns:
            int: The decrypted message.
        """
        a, b = ct
        s = sk
        # Compute the dot product of the secret key and the a vector
        m = np.mod(np.dot(a, s), q)
        # Subtract the dot product from the b vector
        m = np.mod(abs(b - m), q)
        # If the result is quite large, then the bit was 1
        return 1 if m > q // 4 else 0

        
    def encrypt_string(pk, s, q= default_q):
        """Encrypt a string using the LWE cryptosystem.
        Args:
            pk (tuple): The public key.
            s (str): The string to encrypt.
            q (int): The modulus.
        Returns:
            list: A list containing the ciphertext.
        """
        return [LWE.encrypt_bit(pk, int(bit), q) for bit in s]
    
    def decrypt_string(sk, ct, q= default_q):
        """Decrypt a ciphertext using the LWE cryptosystem.
        Args:
            sk (np.array): The secret key.
            ct (list): The ciphertext to decrypt.
            q (int): The modulus.
        Returns:
            str: The decrypted message.
        """
        return ''.join([str(LWE.decrypt_bit(sk, bit, q)) for bit in ct])
    
    def string_to_binary(s):
        """Convert a string to a list of bits.
        Args:
            s (str): The string to convert.
        Returns:
            list: A list containing the bits.
        """
        return ''.join((bin(ord(char))[2:]) for char in s)
    
    def binary_to_string(b):
        """Convert a list of bits to a string.
        Args:
            b (list): The list of bits to convert.
        Returns:
            str: The converted string.
        """
        return ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8))
    
    def encrypt_text(pk, text, q= default_q):
        """Encrypt a text using the LWE cryptosystem.
        Args:
            pk (tuple): The public key.
            text (str): The text to encrypt.
            q (int): The modulus.
        Returns:
            list: A list containing the ciphertext.
        """
        return LWE.encrypt_string(pk, LWE.string_to_binary(text), q)
    
    def decrypt_text(sk, ct, q= default_q):
        """Decrypt a ciphertext using the LWE cryptosystem.
        Args:
            sk (np.array): The secret key.
            ct (list): The ciphertext to decrypt.
            q (int): The modulus.
        Returns:
            str: The decrypted message.
        """
        return LWE.binary_to_string(LWE.decrypt_string(sk, ct, q))

    def encrypt_int(pk, n, q= default_q):
        """Encrypt an integer using the LWE cryptosystem.
        Args:
            pk (tuple): The public key.
            n (int): The integer to encrypt.
            q (int): The modulus.
        Returns:
            list: A list containing the ciphertext.
        """
        return LWE.encrypt_string(pk, bin(n)[2:], q)
    
    def decrypt_int(sk, ct, q= default_q):
        """Decrypt a ciphertext using the LWE cryptosystem.
        Args:
            sk (np.array): The secret key.
            ct (list): The ciphertext to decrypt.
            q (int): The modulus.
        Returns:
            int: The decrypted message.
        """
        return int(LWE.decrypt_string(sk, ct, q), 2)
    
    def encrypt_file(pk, filename, q= default_q):
        """Encrypt a file using the LWE cryptosystem.
        Args:
            pk (tuple): The public key.
            filename (str): The name of the file to encrypt.
            q (int): The modulus.
        Returns:
            list: A list containing the ciphertext.
        """
        with open(filename, 'r') as f:
            return LWE.encrypt_string(pk, f.read(), q)
        
    def decrypt_file(sk, ct, filename, q= default_q):
        """Decrypt a ciphertext using the LWE cryptosystem.
        Args:
            sk (np.array): The secret key.
            ct (list): The ciphertext to decrypt.
            filename (str): The name of the file to decrypt to.
            q (int): The modulus.
        """
        with open(filename, 'w') as f:
            f.write(LWE.decrypt_string(sk, ct, q))