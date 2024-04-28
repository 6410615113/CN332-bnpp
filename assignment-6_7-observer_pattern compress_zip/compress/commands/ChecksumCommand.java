package commands;

import algorithms.ChecksumAlgorithm;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;

public class ChecksumCommand implements Command {
    private ChecksumAlgorithm checksumAlgorithm;

    public ChecksumCommand(ChecksumAlgorithm checksumAlgorithm) {
        this.checksumAlgorithm = checksumAlgorithm;
    }

    @Override
    public void execute(String inputFile, String outputFile) {
        try {
            // Read the content of the input file into a byte array
            byte[] inputBytes = Files.readAllBytes(Paths.get(inputFile));

            // Calculate the checksum using the checksum algorithm
            String checksum = checksumAlgorithm.checksum(inputBytes);

            // Write the checksum to the output file
            try (Writer writer = new FileWriter(outputFile)) {
                writer.write(checksum);
            }

            System.out.println("Checksum calculation completed successfully.");
        } catch (IOException e) {
            e.printStackTrace();
            System.err.println("Error occurred while calculating checksum.");
        }
    }
}
