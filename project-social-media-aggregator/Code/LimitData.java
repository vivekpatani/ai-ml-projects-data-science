import java.util.*;
import java.net.*;
import java.io.*;
import java.sql.*;
class URLInfo
{
	URL url;
	int depth;
	int frequency;
	URLInfo(URL u, int d, int f)
	{
		url = u;
		depth = d;
		frequency = f;
	}
}
class Crawler{
	public static void crawl(String input) throws Exception{
		int threshold = 5;
		File output_file = new File("output.txt");
		BufferedWriter output = new BufferedWriter(new FileWriter(output_file));
		Scanner sc = new Scanner(System.in);
		
		int x=0;
	//	System.out.print("Enter the keyword to search: ");
	//	String input=sc.nextLine();
		String keyword[] = input.split(" ");
		//String keyword = sc.nextLine();
		//URL startUrl = new URL("dnaindia.com");
		Vector<URLInfo> urls = new Vector<URLInfo>(); //TO store all urls
		Vector<URLInfo> key_urls = new Vector<URLInfo>(); //To store urls in which keyword is found
		Vector<URLInfo> searchedurls = new Vector<URLInfo>();
		String seed[]={"http://dnaindia.com/","http://hindustantimes.com/"};
		for(int m=0;m<seed.length;m++)
		{
		URL startUrl = new URL(seed[m]);
		urls.add(new URLInfo(startUrl,0,0));
		}
		//urls.add(startUrl); //Add intial URL
		System.out.println("\nSearched Pages:");
		int frequency =0;
		int count=0;
		outer:
		for (int m=0; m<seed.length;m++){	
			urls.clear();
			URL startUrl = new URL(seed[m]);
			urls.add(new URLInfo(startUrl,0,0));
			int d1c,d2c,d3c;
			int scount =0;
		d1c=d2c=d3c=0;
		while(!urls.isEmpty() && scount<100)//(int i=0;i<urls.size() && i <100 ;i++)
		{
			try{
			sort(urls);
			URLInfo ui = urls.get(0);	
			
			urls.removeElementAt(0);
			URL u = ui.url;
		//	calculatef(ui,keyword);
			frequency = 0;
			Scanner in = new Scanner(u.openStream()); //Get the URL stream into Scanner
			System.out.println(" "+u.toString()+" and depth:"+ui.depth+" and frequency: "+ui.frequency); //Print the current url
			scount++;
			searchedurls.add(ui);
			while(in.hasNextLine() && ui.depth<=3 ){
				if(count>40) break outer;
				String s = in.nextLine();
				for(x=keyword.length-1;x>=0;x--)
				{
				if(!s.contains(keyword[x]))
					break;
				}
				if(x==-1)
					{//If line contains keyword
					frequency++;
					//ui.frequency=frequency;
					if(frequency>threshold  && !checkduplicate(key_urls,ui.url))
					{
						//System.out.println("FREQUENCY"+frequency);
						//ui.frequency = frequency ;
						key_urls.add(ui);
						count++;
					}
				}
				int start=0,end=0;
			pqrs:	while((start=s.indexOf("<a href=\"http://",start))!=-1){ //Find links in the page
					end = s.indexOf("\"",start+9);
					//System.out.println(start+" "+end);
					String new_url = s.substring(start+9,end);//start+9 cz we want to skip first 9 chars which are <a href='
					URLInfo ua = new URLInfo((new URL(new_url)),ui.depth+1,0);
					if(!checkduplicate(searchedurls,ua.url)){
						calculatef(ua,keyword);
					switch(ua.depth)
					{
						case 1: d1c++;
								if(d1c<=5) {urls.add(ua); System.out.println("URl added:"+ua.url.toString());}
								else break pqrs;
								break; 
						case 2: d2c++;
								if(d2c<=5) urls.add(ua);
								else break pqrs;
								break;
						case 3: d3c++;
								if(d3c<=5) urls.add(ua);
								else break pqrs;
								break;
					}
						//urls.add(ua);
					}
					start = end; //Search for new link from end of first
				}
			}
		}catch(Exception e){
			//System.out.println("Server error");	
		}
		}}
		System.out.println();
		if(key_urls.size()==0) System.out.println("Keyword not found");
		else{
			System.out.println("Keyword found at:");
			int i=1;
			for(URLInfo u:key_urls)
			{ //Print all URLs containing the keyword
				output.write((i++)+"	"+input+"	"+u.url.toString());
				output.write("\n");
				System.out.println("("+(i++)+")"+u.url.toString());
				System.out.println(u.frequency); 
			}
		}
		output.flush();
		insertion.insert();
		output.close();
	}	
	public static boolean checkduplicate(Vector<URLInfo> a,URL u)
	{
		for(URLInfo ub:a)
		{
			if(ub.url.toString().equalsIgnoreCase(u.toString()))
				return true;
		}
		return false;
	}
	public static void sort(Vector<URLInfo> a) throws Exception
	{
		int n=a.size();
		 URLInfo temp = new URLInfo(new URL("http://fff.com"),0,0);
        for (int c = 0; c < n-1; c++) {
      for (int d = 0; d < n - c - 1; d++) {
        if (a.get(d).frequency < a.get(d+1).frequency )/* For descending order use < */
        {
        	temp.url = a.get(d).url;
        	temp.depth = a.get(d).depth;
        	temp.frequency = a.get(d).frequency; 
            a.get(d).url = a.get(d+1).url;
        	a.get(d).depth = a.get(d+1).depth;
        	a.get(d).frequency = a.get(d+1).frequency;
          	a.get(d+1).url = temp.url;
          	a.get(d+1).depth = temp.depth;
          	a.get(d+1).frequency =temp.frequency;
        }       
      }
    }
        
	}
	public static void calculatef(URLInfo a,String[] key) throws IOException
	{
		int freq=0;
		URL u = a.url;
		Scanner in = new Scanner(u.openStream()); 
		int x; String s;
		while(in.hasNextLine())
		{
			s = in.nextLine();
			x=0;
			for(x=key.length-1;x>=0;x--)
			{
				if(!s.contains(key[x]))
					{//System.out.println("l4");//If line contains keyword
						break;
					}
			}
			if(x==-1) freq++;
		}
		a.frequency = freq;
	}
}
class insertion
{
	public static void insert() throws Exception
	{
		Class.forName("com.mysql.jdbc.Driver");
		Scanner pin = new Scanner(new File("output.txt"));
		Connection con1= DriverManager.getConnection("jdbc:mysql://localhost:3306/sma","root","");
		Statement st1= con1.createStatement();
	
		while(pin.hasNextLine())
		{
			String line = pin.nextLine();
			String s[] = line.split("\t");
			st1.executeUpdate("INSERT INTO links(keyword,link,date) VALUES ('"+s[1]+"','"+s[2]+"',NOW())");

		}
	}
}