var express = require('express')
var bodyParser = require('body-parser')
var exec = require('child_process').exec;

var app = express()
app.use(bodyParser.json())

app.get('*', function(req, res, next){
    // if(req.headers.host == 'vion-stage.mixd.tv' || req.headers.host == 'localhost:3000')  //if it's a sub-domain
    if(req.headers.host == 'vion-stage.mixd.tv')  //if it's a sub-domain
        req.url = '/vion-stage' + req.url;  //append some text yourself
    next();
});

app.get('/image-import/:imageURL/:titleString/:uuid', function(req, res) {
    var cmd = '/usr/bin/python image_labeler.py --url="http://image.tmdb.org/t/p/original/' +
        req.params.imageURL +
        '" --title="' +
        req.params.titleString
        +
        '" --uuid="' +
        req.params.uuid +
        '"'
    console.log("running: " + cmd)
    exec(cmd, function(error, stdout, stderr) {
        console.log(stdout)
    });

    res.send({
        'result': 'TBD',
        'msg': {
            'img': "would load " + req.params.imageURL,
            'title': "would load " + req.params.titleString
        }
    });
})

app.get('/', function(req, res) {
    res.send({
        'result': 'error',
        'msg': {
            'error': "API endpoint missing"
        }
    });
})



app.listen(9756, function(){
    console.log('Server listening on', 9756)
})
