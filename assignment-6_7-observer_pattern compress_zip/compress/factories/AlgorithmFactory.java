package factories;

import algorithms.*;

public class AlgorithmFactory {
    public static CompressionAlgorithm createCompressionAlgorithm(String algorithm) {
        switch (algorithm.toLowerCase()) {
            case "zip":
                return new ZipCompression();
            // Add cases for other compression algorithms if needed
            default:
                throw new IllegalArgumentException("Unsupported compression algorithm: " + algorithm);
        }
    }

    public static EncryptionAlgorithm createEncryptionAlgorithm(String algorithm) {
        switch (algorithm.toUpperCase()) {
            case "DES":
                return new DESAlgorithm();
            // Add cases for other encryption algorithms if needed
            default:
                throw new IllegalArgumentException("Unsupported encryption algorithm: " + algorithm);
        }
    }

    public static ChecksumAlgorithm createChecksumAlgorithm(String algorithm) {
        switch (algorithm.toUpperCase()) {
            case "MD5":
                return new MD5Checksum();
            // Add cases for other checksum algorithms if needed
            default:
                throw new IllegalArgumentException("Unsupported checksum algorithm: " + algorithm);
        }
    }
}
