const express = require('express');
const concat = require('concat-stream');
const parseArgs = require('minimist');
const solve = require('./solve');

const app = express();

app.use(function(req, res, next){
    req.pipe(concat(function(data){
        req.body = data;
        next();
    }));
});

app.post('/solve', function (req, res) {
    const url = req.query.url;
    const html = req.body;
    const solution = solve(url, html);
    res.send(solution);
});

const argv = parseArgs(process.argv.slice(2), {
    default: {
        port: 8081,
        host: 'localhost',
    },
});

app.listen(argv.port, argv.host, (err) => {
    if (err) {
        console.log(err)
    } else {
        console.log(`Listening on ${argv.host}:${argv.port}`);
    }
});
