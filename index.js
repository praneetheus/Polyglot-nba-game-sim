var express = require('express')
var app = express()
// const http = require('http').Server(app)
const port = 5000
const spawn = require('child_process').spawn

var bodyParser = require('body-parser');
app.use(bodyParser.json());

// function to call python script
// function callPython() {
//     const proc = spawn('python3', ['./h.py'])
//     let d; 
//     proc.stdout.on('data', data => {
//         // console.log(data.toString()); 
//         d = data.toString()
//         return d
//     })
// }


app.use(express.static(__dirname + "/public"))

// console.log("Hello")

// Handling POST request
app.post(['/', '/index.html'], function(req, res) {
    // console.log(req.body.teamA);
    // console.log(req.body.teamB);
    // console.log(req.body.model);
    const model = req.body.model; 

    if (model == 1) {
        const proc = spawn('python3', ['./model1.py', req.body.teamA, req.body.teamB])
        let d; 
        proc.stdout.on('data', data => {
            // console.log(data.toString()); 
            d = data.toString()
            // console.log(d)
            res.send(JSON.stringify(d));
        })
    }
    if (model == 2) {
        const proc = spawn('python3', ['./model2.py', req.body.teamA, req.body.teamB])
        let d; 
        proc.stdout.on('data', data => {
            // console.log(data.toString()); 
            d = data.toString()
            // console.log(d)
            res.send(JSON.stringify(d));
        })
    }

    if (model ==3) {
        const proc = spawn('python3', ['./model3.py', req.body.teamA, req.body.teamB])
        let d; 
        proc.stdout.on('data', data => {
            // console.log(data.toString()); 
            d = data.toString()
            // console.log(d)
            res.send(JSON.stringify(d));
        })
    }
    
    // let resData 
    // let ret = callPython()
    // console.log(typeof(ret))
    // res.send(JSON.stringify(ret));
    
});


// http.listen(port, () => console.log(`Active on ${port} port`))
// app.listen(port, '0.0.0.0', () => console.log(`Active on ${port} port`))
app.listen(port, '0.0.0.0', () => console.log(`Active on ${port} port`))