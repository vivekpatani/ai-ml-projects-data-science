import java.util.Timer;
public class Loop 
{
	public static void main(String args[]) throws InterruptedException 
	{
		Timer time = new Timer(); 
		Multiple st = new Multiple();
		time.schedule(st, 0, 1000*30);
	}
}