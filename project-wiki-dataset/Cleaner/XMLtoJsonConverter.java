import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import org.apache.commons.io.IOUtils;
import org.json.JSONObject;
import org.json.XML;



public class XMLtoJsonConverter {
    private URL url = null;
    private InputStream inputStream = null;   
    public void getXMLfromJson() {
        try{
            url = XMLtoJsonConverter.class.getClassLoader().getResource("file3.xml");
            //System.out.println(url);
            inputStream = url.openStream();
            
            String xml = IOUtils.toString(inputStream);
            //System.out.println(xml);
            JSONObject xmlJSONObj = XML.toJSONObject(xml);
            String jsonString = xmlJSONObj.toString(4);
            System.out.println(jsonString);
            //JSON objJson = new XMLSerializer().read(xml);
            //System.out.println("JSON data : " + objJson);
        }catch(Exception e){
            e.printStackTrace();
        }finally{
     try {
                if (inputStream != null) {
                    inputStream.close();
                }
                url = null;
            } catch (IOException ex) {}
        }
    }
    public static void main(String[] args) {
    	
        new XMLtoJsonConverter().getXMLfromJson();
    }
}

