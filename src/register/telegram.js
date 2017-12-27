//This is a module file for the IoP Community Bot on Telegram. It is not a full Telegram bot.

var request = require("request-promise-native");

async function handleMsg(msg, chatInterface) {
    msg = msg.text.substring(2, msg.text.length).split(" ").filter((item, index, inputArray) => {
        return item !== "";
    });

    switch(msg[0]) {
        case "register":
            if (msg.length !== 4) {
                return "You have the wrong amount of arguments. Run /%help.";
            }

            try {
                return (await request({
                    method: "POST",
                    uri: "http://URL:PORT/register",
                    body: {
                        iop: msg[1],
                        eth: msg[2],
                        sig: msg[3]
                    },
                    json: true
                }));
            } catch(e) {
                return e.response.body;
            }
            break;

        case "help":
            return "Want to claim your Hydra tokens? Tell me \"/%register IOP_ADDRESS ETH_ADDRESS SIGNED_ETH_ADDRESS\"";
            break;
    }
}

module.exports = {
    handleMsg: handleMsg
};
