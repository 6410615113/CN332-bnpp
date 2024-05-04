import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Clock clock = new Clock();
        Scanner sc = new Scanner(System.in);

        clock.addObserver(new ButtonObserver() {
            @Override
            public void shortPress() {
                if (clock.isCountingDown()) {
                    clock.stopCountdown();
                } else {
                    clock.startCountdown();
                }
            }

            @Override
            public void longPress() {
                clock.increasePresetTime();
            }
        });

        while (true) {
            System.out.println("Enter 'display' to show current time, \n'short' to start/stop countdown, \n 'long' to increase preset time:");
            String input = sc.nextLine();

            switch (input) {
                case "display":
                    clock.displayCurrentTime();
                    break;
                case "short":
                    clock.shortPress();
                    break;
                case "long":
                    clock.longPress();
                    break;
                default:
                    System.out.println("Invalid input. Please enter 'display', 'short', or 'long'.");
            }
        }
    }
}
