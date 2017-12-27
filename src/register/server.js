var Web3 = require("web3");
var web3 = new Web3();
delete Web3;

var client = new (require("bitcoin")).Client({
    host: "localhost",
    port: 8337,
    user: "USERNAME",
    pass: "PASSWORD"
});

var mysql = require("mysql").createConnection({
  host: "localhost",
  user: "USERNAME",
  password: "PASSWORD",
  database: "DATABASE"
});
mysql.connect();

var data = JSON.parse(require("fs").readFileSync("../data/snapshot.json"));

var express = require("express")();
express.use(require("body-parser").json());
express.post("/register", async (req, res) => {
    if (!(web3.utils.isAddress(req.body.eth))) {
        res.status(400);
        res.end("That ETH address is invalid.");
        return;
    }

    if (!(data[req.body.iop])) {
        res.status(400);
        res.end("That IoP address isn't on the list of IoP addresses eligible for this airdrop. Sorry.");
        return;
    }

    client.verifyMessage(req.body.iop, req.body.sig, req.body.eth, async (err, valid, resHeaders) => {
        if (valid) {
            mysql.query("SELECT * FROM TABLE WHERE iop=?", [req.body.iop], async (err2, res2, info) => {
                if (res2.length !== 0) {
                    res.status(400);
                    res.end("You have already registered.");
                    return;
                }
                res.status(200);
                res.end("You have successfully registered! You have " + Math.min(Math.floor(data[req.body.iop]/2), 250) + " tickets!");
                mysql.query("INSERT INTO TABLE VALUES (?, ?, ?)", [req.body.iop, req.body.eth, req.body.sig], async (err)=>{});
            });
        } else {
            res.status(400);
            res.end("That signature is not a signed version of that Ethereum address, from the specified IoP address.");
        }
    });
});

express.listen(8080, async () => {
    console.log("Listening.");
});
