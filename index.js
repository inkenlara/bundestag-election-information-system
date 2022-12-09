const express = require('express')


const app = express()
const port = 3000

app.listen(port, () => console.info("listening"))


app.use(express.static(__dirname + '/public/'))
app.use('/css', express.static(__dirname + 'public/css/'))
app.use('/js', express.static(__dirname + 'public/js/'))
app.use('/img', express.static(__dirname + 'public/img/'))

app.get('', (req, res) => {
    res.sendFile(__dirname + '/public/views/index.html')
})





/* const http = require('http')
const fs = require('fs')
const port = 3000


const server = http.createServer(function(req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'})
    fs.readFile('index.html', function(error, data) {
        if(error) {
            res.writeHead(404)
            res.write("File not found")
        } else {
            res.write(data)
        }
        res.end()
    })
})

server.listen(port, function(error) {
    if(error) {
        console.log("Error", error)
    } else {
        console.log("Server running")
    }
})*/ 