const fs = require('fs')

let intros = fs.readFileSync('src/intros.txt', 'UTF-8').split(/\r?\n/) // create array from text file of intros, separating on newline
let content = fs.readFileSync('src/content.txt', 'UTF-8').split(/\r?\n/) // create array from text file of content, separating on newline

module.exports = {
    async getRandomPost() { // picks a random intro and content to post, concatenates and returns them
        const random1 = Math.floor(Math.random() * intros.length) // pick a random number according to length of intros array
        const random2 = Math.floor(Math.random() * content.length) // pick a random number according to length of content array
        // Below lines will use the two random numbers to pick intro and content from the matching array locations and concatenate them
        return (intros[random1] + "\n\n" + content[random2]).toString() // return text to be posted
    }
}