package algorithms;

import java.security.MessageDigest;

public class MD5Checksum implements ChecksumAlgorithm {
    @Override
    public String checksum(byte[] data) {
        try {
            // Get an instance of the MD5 message digest algorithm
            MessageDigest md = MessageDigest.getInstance("MD5");

            // Update the message digest with the input data
            md.update(data);

            // Compute the MD5 hash value
            byte[] digest = md.digest();

            // Convert the byte array to a hexadecimal string representation
            StringBuilder hexString = new StringBuilder();
            for (byte b : digest) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }

            return hexString.toString();
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
