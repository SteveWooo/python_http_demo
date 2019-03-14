const express = require("express");
const bodyParser = require('body-parser')
const app = express();

app.use(bodyParser.json());
app.use(express.static('static'));

app.post('/add_1', function(req, res){
	var body = req.body;
	body.number += 100;
	res.send(JSON.stringify({
		number : body.number
	}))
})

app.listen("8000");