const express = require('express')
const controller = require('./controller')

const app = express()

app.use(express.json())

app.get('/getConnectedDevices', controller.getConnectedDevices)

const PORT = process.env.PORT || 3401
app.listen(PORT, () => {
    console.log("Server listening on PORT: ", PORT)
})