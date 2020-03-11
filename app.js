data = require("./lib/datahub.js")
const express = require('express');
const app = express();
app.use(express.static('assets'));


data.updateData()
// setInterval(function(){
//     console.log(data.compareData);
// }, 2000);



app.get('/compareData.js', (req, res) => {
    res.send(data.compareData);
});

app.listen(3000, () => console.log('Listening on port 3000!'));
