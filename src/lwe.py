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
    