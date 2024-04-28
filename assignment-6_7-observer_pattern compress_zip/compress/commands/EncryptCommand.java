package commands;

import algorithms.EncryptionAlgorithm;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;

public class EncryptCommand implements Command {
    private EncryptionAlgorithm encryptionAlgorithm;

    public EncryptCommand(EncryptionAlgorithm encryptionAlgorithm) {
        this.encryptionAlgorithm = encryptionAlgorithm;
    }

    @Override
    public void execute(String inputFile, String outputFile) {
        try {
            // Read the content of the input file into a byte array
            byte[] inputBytes = Files.readAllBytes(Paths.get(inputFile));

            // Encrypt the byte array using the encryption algorithm
            byte[] encryptedBytes = encryptionAlgorithm.encrypt(inputBytes);

            // Write the encrypted data to the output file
            try (OutputStream outputStream = new FileOutputStream(outputFile)) {
                outputStream.write(encryptedBytes);
            }

            System.out.println("Encryption completed successfully.");
        } catch (IOException e) {
            e.printStackTrace();
            System.err.println("Error occurred while encrypting the file.");
        }
    }
}
