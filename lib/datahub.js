const {spawn} = require('child_process');


exports.compareData = 'hi'
exports.updateData = function(){

    var countryData = [];
    // spawn new child process to call the python script
    const python = spawn('python', ['python/compareCountry.py']);

    // collect data from script
    python.stdout.on('data', function (data) {
     console.log('Pipe data from python script ...');
     countryData.push(data);
    });

    // in close event we are sure that stream is from child process is closed
    python.on('close', (code) => {
        exports.compareData = 'let compareData = ' + countryData.join("");//JSON.parse(countryData.join(""));
        console.log(`child process close all stdio with code ${code}`);
    });


}






