import java.util.*;
import java.sql.*;
import java.io.*;
import java.net.*;
public class Multiple extends TimerTask
{
	public void run()
	{
		try
		{
		int x=0;
	
		Crawler c= new Crawler();
		String input1[] = new String[10];
		x = extraction.extract(input1);
		System.out.println(x);
		for(int i=0;i<x;i++)
		{
			System.out.println(input1[i]);
			c.crawl(input1[i]);
		}
		
	}catch(Exception e){};
	}
}
class extraction
{
	public static int extract(String[] ip) throws Exception
	{
		Class.forName("com.mysql.jdbc.Driver");
		Connection con1= DriverManager.getConnection("jdbc:mysql://localhost:3306/sma1","root","");
		Statement st1= con1.createStatement();
		String sql1 = "SELECT * FROM sensitive_words";
		ResultSet rs = st1.executeQuery(sql1);
		int ik=0;
		while(rs.next())
		{
			String word = rs.getString("Word");
			ip[ik]=word;
			ik++;
		}
		return ik;
	}
}