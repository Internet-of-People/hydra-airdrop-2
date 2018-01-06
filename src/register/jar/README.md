# ClaimAirdrop.jar

This is a tool that goes through all your addresses and registers for each one.

To compile it:

- Download this folder and `cd` into it.
- Get all the dependencies in jar format (Apache HttpCore, HttpClient, and Apache Commons Codec/Logging):

```
commons-codec-1.11.jar

commons-logging-1.2.jar

httpclient-4.5.4.jar

httpclient-cache-4.5.4.jar

httpclient-win-4.5.4.jar

httpcore-4.4.7.jar

httpcore-ab-4.4.8.jar

httpcore-nio-4.4.8.jar

httpmime-4.5.4.jar
```

- `javac -cp ./* ./ClaimAirdrop.java`
- Extract the contents of every jar to that folder.
- Package it with `jar cfm ClaimAirdrop.jar .\Manifest.mf com .\ClaimAirdrop.class`.

To run it:

- Boot your IoP Node with `-server -rpcuser=USER -rpcpassword=PASS` Feel free to change USER/PASS to something else.
- Go to where the jar is.
- java -jar ClaimAirdrop.jar
- Enter your Ethereum address
- Enter USER (or what you set the user to).
- Enter PASS (or what you set the pass to).
- Wait a few seconds.
- See the results for each of your addresses.

You can likely find your IoP Node software in `C:\Program Files\IoP\daemon` on Windows or `/usr/local/bin` on Linux. The full command would be `./iopd -server -rpcuser=USER -rpcpassword=PASS`. On Windows, it isn't `./iopd` but rather `.\iopd.exe`. Close any other instance of the IoP Node software first, and when you're done with using the jar, hit `Ctrl` + `C` to close out of the software. Then use your IoP software as you normally would.
