// load Balancer Upstream API


var express = require('express');
var bodyParser = require('body-parser');
var cors = require('cors')
var request = require('request');

var app = express();

// CORS
app.options('*', cors())

// port & hostname
var port = 3437;
var hostname = "http://monty.link:3436";

// middleware

	// bodyParser
	app.use(bodyParser.json());
	app.use(bodyParser.urlencoded({extended:false}));

	//CORS

	app.use(function(req, res, next) {
  	res.header("Access-Control-Allow-Origin", "*");
  	res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  	next();
	});


	// catch errors

	app.use(function (error, req, res, next) {
  		if (error instanceof SyntaxError) {
  			// Syntax Error
    		res.status(400);
    		res.json({code:400,message:"Malformed request. Check and try again."});
  		} else {
  			// Other error
  			res.status(400);
  			res.json({code:400,message:"There was a problem with your request."});
    	next();
  	}
});

// catch-all route
app.all('*',(req,res)=>{
  request({url:hostname+req.url,method:req.method,json:true,body:req.body},(error,response,body)=>{
    res.json(response.body)
  });
});


app.listen(port,()=>{
	console.log('server running on port '+port);
});
