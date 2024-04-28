package main;

import algorithms.*;
import commands.*;
import factories.AlgorithmFactory;

public class CommandLineParser {
    public static void main(String[] args) {
        if (args.length < 4) {
            System.err.println("Usage: java CommandLineParser <inputFile> <-compressionAlgorithm> <-encryptionAlgorithm> <-checksumAlgorithm>");
            return;
        }

        String inputFile = args[0];
        String compressionAlgorithm = args[1].substring(1); // Remove leading '-'
        String encryptionAlgorithm = args[2].substring(1); // Remove leading '-'
        String checksumAlgorithm = args[3].substring(1); // Remove leading '-'

        // Instantiate appropriate algorithms based on user input
        CompressionAlgorithm compression = AlgorithmFactory.createCompressionAlgorithm(compressionAlgorithm);
        EncryptionAlgorithm encryption = AlgorithmFactory.createEncryptionAlgorithm(encryptionAlgorithm);
        ChecksumAlgorithm checksum = AlgorithmFactory.createChecksumAlgorithm(checksumAlgorithm);

        // Execute commands
        executeCompression(inputFile, compression);
        executeEncryption(inputFile, encryption);
        executeChecksum(inputFile, checksum);
    }

    private static void executeCompression(String inputFile, CompressionAlgorithm compression) {
        CompressCommand compressCommand = new CompressCommand(compression);
        String outputFile = inputFile + ".compressed";
        compressCommand.execute(inputFile, outputFile);
    }

    private static void executeEncryption(String inputFile, EncryptionAlgorithm encryption) {
        EncryptCommand encryptCommand = new EncryptCommand(encryption);
        String outputFile = inputFile + ".encrypted";
        encryptCommand.execute(inputFile, outputFile);
    }

    private static void executeChecksum(String inputFile, ChecksumAlgorithm checksum) {
        ChecksumCommand checksumCommand = new ChecksumCommand(checksum);
        String outputFile = inputFile + ".checksum";
        checksumCommand.execute(inputFile, outputFile);
    }
}
