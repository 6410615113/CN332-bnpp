import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.ArrayList;

interface ButtonObserver {
    void shortPress();

    void longPress();
}

public class Clock {
    private static final int INITIAL_PRESET_TIME = 10; // Initial preset time in minutes
    private static final int MAX_PRESET_TIME = 60; // Maximum preset time in minutes

    private int presetTime; // in minutes
    private int remainingTime; // in seconds
    private boolean countingDown;
    private List<ButtonObserver> observers;

    public Clock() {
        this.presetTime = INITIAL_PRESET_TIME;
        this.countingDown = false;
        this.observers = new ArrayList<>();
    }

    public void addObserver(ButtonObserver observer) {
        observers.add(observer);
    }

    public void removeObserver(ButtonObserver observer) {
        observers.remove(observer);
    }

    public void notifyShortPress() {
        for (ButtonObserver observer : observers) {
            observer.shortPress();
        }
    }

    public void notifyLongPress() {
        for (ButtonObserver observer : observers) {
            observer.longPress();
        }
    }

    public void shortPress() {
        notifyShortPress();
    }

    public void longPress() {
        notifyLongPress();
    }

    public boolean isCountingDown() {
        return countingDown;
    }

    public void increasePresetTime() {
        if (presetTime < MAX_PRESET_TIME) {
            presetTime+=10;
            System.out.println("Preset time increased to " + presetTime + " minutes.");
        } else {
            presetTime = INITIAL_PRESET_TIME; // Reset to initial time if maximum reached
            System.out.println("Preset time reset to " + INITIAL_PRESET_TIME + " minutes.");
        }
    }

    private void displayRemainingTime() {
        int minutes = remainingTime / 60;
        int seconds = remainingTime % 60;
        System.out.printf("Remaining time: %02d:%02d\n", minutes, seconds);
    }

    public void startCountdown() {
        if (!countingDown) {
            countingDown = true;
            System.out.println("Countdown started for 1 minutes.");
            displayCurrentTime();
            new Thread(() -> {
                for (int i = 60; i > 0; i--) {
                    remainingTime = i;
                    displayRemainingTime();
                    try {
                        TimeUnit.SECONDS.sleep(1); // Wait for 1 second
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                countingDown = false;
                System.out.println("Countdown finished.");
                displayCurrentTime();
            }).start();
        } else {
            System.out.println("Countdown is already in progress.");
        }
    }

    public void stopCountdown() {
        if (countingDown) {
            countingDown = false;
            System.out.println("Countdown stopped.");
            // Add code to stop countdown
        } else {
            System.out.println("Countdown is not in progress.");
        }
    }

    public void displayCurrentTime() {
        LocalTime currentTime = LocalTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm:ss");
        String formattedTime = currentTime.format(formatter);
        System.out.println("Current time: " + formattedTime);
    }

}