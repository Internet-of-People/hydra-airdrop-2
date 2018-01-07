# ClaimAirdrop.jar

## HASHES:

### MD5: af7178c691d6d4a493be4bb51f9ea665

### SHA-1: 3b9429b52bb42c1f423a2bc6fdb9a5fd420cdf60

This is a tool that goes through all your addresses and registers for each one.

To run it:

- On Windows, open File Explorer. Type into the address bar `%APPDATA%`. Then open `IoP`. On Linux, open `~/.iop`. On MacOS, open `~/Library/Application Support/IoP`.
- Edit `iop.conf`. If it doesn't exist, make it. Make sure it has the lines:
```
server=1
rpcuser=USER
rpcpassword=PASS
```

Feel free to change USER/PASS to something else.

- Reboot your IoP Software.
- Go to where the jar is.
- `java -jar ClaimAirdrop.jar`
- Enter your Ethereum address
- Enter USER (or what you set the user to).
- Enter PASS (or what you set the pass to).
- Wait a few seconds.
- See the results for each of your addresses.
- Go back to the `iop.conf` file.
- Remove the lines we added.
- Reboot your node software.

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
- Package it with `jar cfm ClaimAirdrop.jar .\Manifest.mf org .\ClaimAirdrop.class`.
