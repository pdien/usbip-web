const { promisify } = require('util')
const exec = promisify(require('child_process').exec)

exports.getConnectedDevices = async (req, res) => {
    const output = await exec('usbip list -l')
    console.log(output)
    res.send(output.stdout)
}
