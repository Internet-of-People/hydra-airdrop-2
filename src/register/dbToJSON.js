var mysql = require("mysql").createConnection({
    host: "localhost",
    user: "USERNAME",
    password: "PASSWORD",
    database: "DATABASE"
});
mysql.connect();

var data = {};
mysql.query("SELECT * FROM TABLE", async (err, res, info) => {
    res.forEach((row) => {
        data[row.iop] = {
            eth: row.eth,
            sig: row.sig
        };
    });
    require("fs").writeFileSync("../data/registered.json", JSON.stringify(data));
});
mysql.end();
