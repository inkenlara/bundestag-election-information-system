/* 
const {Client} = require('pg')

const client = new Client({
    host: "localhost",
    user: "postgres",
    port: "5432",
    password: "",
    database: "wahl"
})

function get_data(query) {
    client.connect()

    client.query(`SELECT * FROM strukturdaten`, (err, res) => {
        if(!err) {
            let data = JSON.stringify(res.rows);
            console.log(data)
        } else {
            console.log(err.message)
        }
        client.end;
    })
} */
