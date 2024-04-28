package commands;

import algorithms.CompressionAlgorithm;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;

public class CompressCommand implements Command {
    private CompressionAlgorithm compressionAlgorithm;

    public CompressCommand(CompressionAlgorithm compressionAlgorithm) {
        this.compressionAlgorithm = compressionAlgorithm;
    }

    @Override
    public void execute(String inputFile, String outputFile) {
        try {
            // Read the content of the input file into a byte array
            byte[] inputBytes = Files.readAllBytes(Paths.get(inputFile));

            // Compress the byte array using the compression algorithm
            byte[] compressedBytes = compressionAlgorithm.compress(inputBytes);

            // Write the compressed data to the output file
            try (OutputStream outputStream = new FileOutputStream(outputFile)) {
                outputStream.write(compressedBytes);
            }

            System.out.println("Compression completed successfully.");
        } catch (IOException e) {
            e.printStackTrace();
            System.err.println("Error occurred while compressing the file.");
        }
    }
}
