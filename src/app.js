require('dotenv').config()
const posts = require('./tools/posts')
const mastoapi = require('./tools/mastoapi.js')
const fs = require('fs')
const command = process.env.COMMAND || "/post"
const interval = process.env.INTERVAL || 86400000
const replyInterval = process.env.REPLY_INTERVAL || 5000

console.log('💬 postodon is running!')

async function replyWithPrompt() {
    const notifications = await mastoapi.getNotifications(5) // get the last five notifications
    
    try {
        if (!notifications) throw "No notifications found, moving on..."
        let toReply = notifications.filter(function(status) { //Adds notification to be replied to if below is true
            if (status.content.includes(` ${command}`) && repliedTo.some(i => i.id.includes(status.id)) === false){
                return true // check if notification content contains the set command and has not been replied to
            }
        })
        await toReply.map(async function(status) { // for each toReply status, execute below
            let toMention = '@' + status.account.acct
            if (status.mentions) { // Mention anyone
                toMention = toMention.concat(' ' + status.mentions.map(x => '@' + x.acct).join(" ")) // concatenate mentions with a space
            }
            const randomPost = await posts.getRandomPost()
            mastoapi.postStatus( toMention + ' ' + randomPost, 'reply',status.visibility, status.id) //reply with random post and mentions
            fs.appendFile('postodon.log',`${new Date} - Replied - "${toMention} ${randomPost}"\n`, function(err){
                if(err) console.log(err)
                console.log(`${new Date} - Replied - "${toMention} ${randomPost}"`)
                
            })
        })
        repliedTo = repliedTo.concat(toReply) // add status to list of already replied to statuses
    } catch(err) {
        console.log(err)
    }
}

async function postStatus() { // post a random post
    const randomPost = await posts.getRandomPost()
    const post = await mastoapi.postStatus((randomPost), 'post', 'public')
    fs.appendFile('postodon.log',`${new Date} - Posted - "${randomPost}\n`, function(err){
        if(err) console.log(err)
        console.log(`${new Date} - Posted - "${randomPost}"`)
        
    })
    return post
}

mastoapi.clearNotifications()
let repliedTo = []
setInterval(() => {replyWithPrompt()},replyInterval) //check for commands every 5 seconds
setInterval(() => {postStatus()},interval) // post once a day
