package algorithms;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.DESKeySpec;

public class DESAlgorithm implements EncryptionAlgorithm {
    private static final String ALGORITHM = "DES";

    @Override
    public byte[] encrypt(byte[] data) {
        try {
            // Generate a DES key from a byte array
            byte[] keyData = "YourSecretKey".getBytes(); // Replace "YourSecretKey" with your actual secret key
            DESKeySpec desKeySpec = new DESKeySpec(keyData);
            SecretKeyFactory keyFactory = SecretKeyFactory.getInstance(ALGORITHM);
            SecretKey secretKey = keyFactory.generateSecret(desKeySpec);

            // Initialize the DES cipher in encryption mode
            Cipher cipher = Cipher.getInstance(ALGORITHM);
            cipher.init(Cipher.ENCRYPT_MODE, secretKey);

            // Encrypt the data
            byte[] encryptedData = cipher.doFinal(data);

            // Return the encrypted data
            return encryptedData;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
