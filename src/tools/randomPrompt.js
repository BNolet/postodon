const fs = require('fs')

let intros = fs.readFileSync('src/intros.txt', 'UTF-8').split(/\r?\n/)
let prompts = fs.readFileSync('src/prompts.txt', 'UTF-8').split(/\r?\n/)

module.exports = {
    async getRandomPrompt() {
        const random1 = Math.floor(Math.random() * intros.length)
        const random2 = Math.floor(Math.random() * prompts.length)
        console.log(intros[random1] + "\n\n" + prompts[random2])
        return (intros[random1] + "\n\n" + prompts[random2]).toString()
    }
}