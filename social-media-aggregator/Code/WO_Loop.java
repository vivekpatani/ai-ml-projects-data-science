import java.util.Timer;
public class Loop 
{
	public static void main(String args[]) throws InterruptedException 
	{
		Timer time = new Timer(); // Instantiate Timer Object
		Multiple st = new Multiple(); // Instantiate SheduledTask class
		time.schedule(st, 0, 1000*60*60); // Create Repetitively task for every 1 secs
	}
}