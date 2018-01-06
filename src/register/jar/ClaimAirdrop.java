import java.util.Scanner; 
import java.util.Arrays;

import org.apache.http.impl.client.HttpClients;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.util.EntityUtils;

public class ClaimAirdrop {
    static final String airdropServerURL = "http://35.196.92.242:8081/register";
    
    static String ethAddress, iopUsername, iopPassword;
    
    static CloseableHttpClient httpClient;
    
    static HttpPost iopPost;
    static HttpPost serverPost;
    
    public static void register(String iop, String sig) throws Exception {
        //Set a JSON Content-type.
        serverPost.setHeader("Content-type", "application/json");
        //Craft the JSON object.
        serverPost.setEntity(new StringEntity("{\"iop\": \"" + iop + "\", \"eth\": \"" + ethAddress + "\", \"sig\": \"" + sig + "\"}"));
        //Print the server's response.
        System.out.println(EntityUtils.toString(httpClient.execute(serverPost).getEntity()));
        
        //This println is for debugging. It prints the JSON object.
        //System.out.println("{\"iop\": \"" + iop + "\", \"eth\": \"" + ethAddress + "\", \"sig\": \"" + sig + "\"}");
    }
    
    public static String signFrom(String iop) throws Exception {
        //Make sure the address is ours.
        iopPost.setEntity(new StringEntity("{\"jsonrpc\": \"1.0\", \"id\":\"1\", \"method\": \"validateaddress\", \"params\": [\"" + iop + "\"]}"));   
        if (EntityUtils.toString(httpClient.execute(iopPost).getEntity()).split("ismine\":")[1].replaceAll(" ", "").substring(0, 4).equals("true")) {
            //Craft the signmessage call.
            iopPost.setEntity(new StringEntity("{\"jsonrpc\": \"1.0\", \"id\":\"1\", \"method\": \"signmessage\", \"params\": [\"" + iop + "\", \"" + ethAddress + "\"]}"));
            //Execute it, get the result, split along ", and return the third object (which is the signature).
            //We likely should make this not hard coded...
            return EntityUtils.toString(httpClient.execute(iopPost).getEntity()).split("\"")[3];
        } else {
            return "";
        }
    }
    
    //Takes args in case we add command line arguments as an alternative option to the terminal prompts.
    public static void getGlobalVars(String[] args) {
        Scanner scan = new Scanner(System.in);
        
        //Get the Ethereum address.
        System.out.println("What is your Ethereum address?");
        ethAddress = scan.next();
        //Verify Ethereum address's integrity.
        String eth = ethAddress.toLowerCase();
        //Remove the 0x.
        if (eth.substring(0, 2).equals("0x")) {
            eth = eth.substring(2, eth.length());
        }
        //Make sure it is solely hexidecimal and 40 long.
        if (!eth.matches("[0-9a-f]{40}")) {
            System.out.println("That's an invalid Ethereum address.");
            System.exit(-1);
        }
        //TODO: Add Checksum checking.
        
        //Get the RPC Username.
        System.out.println("What is your IoP RPC Username?");
        iopUsername = scan.next();
        
        //Get the RPC Password.
        System.out.println("What is your IoP RPC Password?");
        iopPassword = scan.next();
        
        System.out.println("Thanks! Please wait a second. If I pause for more than 10 seconds, please hit enter again.");
    }
    
    public static void main(String[] args) throws Exception {
        //Get the Ethereum address and login info.
        getGlobalVars(args);
        
        //Create the HTTP Client.
        httpClient = HttpClients.createDefault();
        //Initialize the HttpPost object pointed to the IoP node that we will reuse.        
        iopPost = new HttpPost("http://" + iopUsername + ":" + iopPassword + "@localhost:8337");
        //Initialize the HttpPost object pointed to the registration server that we will reuse. This is here so we don't make a new one on every register().
        serverPost = new HttpPost(airdropServerURL);
        
        //Make sure we can connect to the node.
        iopPost.setEntity(new StringEntity("{\"jsonrpc\": \"1.0\", \"id\":\"0\", \"method\": \"getinfo\", \"params\": []}"));
        try {
            if (httpClient.execute(iopPost).getStatusLine().getStatusCode() != 200) {
                System.out.println("You gave me the wrong username and password. Please fix this and try again.");
                System.exit(-2);
            }
        } catch(Exception e) {
            e.printStackTrace();
            System.out.println("Your IoP node isn't listening on port 8337. Do you have the server flag enabled?");
            System.exit(-3);
        }
        
        //Call listaddressgroupings.
        iopPost.setEntity(new StringEntity("{\"jsonrpc\": \"1.0\", \"id\":\"0\", \"method\": \"listaddressgroupings\", \"params\": []}"));
        String iopRes = EntityUtils.toString(httpClient.execute(iopPost).getEntity());
        
        //Make sure we have addresses to work with.
        if (iopRes.replaceAll(" ", "").contains("\"result\":[]")) {
            System.out.println("You have no addresses to claim the airdrop with.");
            System.exit(-4);
        }
        
        //Get rid of everything before the array.
        iopRes = "[" + iopRes.split("\\[", 2)[1];
        //Get rid of everything after the array by cutting of the length of the last element of a split on "]". This likely isn't needed but doesn't hurt.
        iopRes = iopRes.substring(0, iopRes.length() - iopRes.split("\\]")[iopRes.split("\\]").length-1].length());
        
        //Make each array part start with an address.
        String[] addressesWithJunk = iopRes.split("\"p");
        //Get rid of the array part that came before the first _"p_.
        String[] addresses = Arrays.copyOfRange(addressesWithJunk, 1, addressesWithJunk.length);
        
        //Print out how many addresses we're working with.
        System.out.println("Claiming on behalf of " + addresses.length + " addresses.");
        
        //Go through each address.
        for (int i = 0; i < addresses.length; i++) {
            //Put the "p" back in, cut off everything after, and including, the " (leaving us with just the address).
            addresses[i] = "p" + addresses[i].split("\"")[0];
            //Register that address, with the Ethereum Address (global var so it's not passed), with the signature generated with signFrom.
            String sig = signFrom(addresses[i]);
            if (sig.equals("")) {
                System.out.println("This address is imported, not ours.");
                continue;
            }
            register(addresses[i], sig);
        }
    }
}
