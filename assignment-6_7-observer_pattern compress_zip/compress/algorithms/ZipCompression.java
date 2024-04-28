package algorithms;

import java.io.ByteArrayOutputStream;
import java.util.zip.Deflater;
import java.util.zip.DeflaterOutputStream;

public class ZipCompression implements CompressionAlgorithm {
    @Override
    public byte[] compress(byte[] data) {
        try {
            // Create a Deflater object with default compression level
            Deflater deflater = new Deflater();

            // Set input data to be compressed
            deflater.setInput(data);

            // Create a byte array output stream to store compressed data
            ByteArrayOutputStream outputStream = new ByteArrayOutputStream(data.length);

            // Create a DeflaterOutputStream to write compressed data to the output stream
            DeflaterOutputStream deflaterOutputStream = new DeflaterOutputStream(outputStream, deflater);

            // Write compressed data to the output stream
            deflaterOutputStream.write(data);

            // Finish writing compressed data
            deflaterOutputStream.finish();

            // Close the output stream
            deflaterOutputStream.close();

            // Return the compressed data as a byte array
            return outputStream.toByteArray();
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
