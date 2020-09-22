const axios = require('axios').default
const uuidv4 = require('uuid').v4
const fs = require('fs')
const url = process.env.INSTANCE_URL
const token = process.env.ACCESS_TOKEN
let uuid = uuidv4()
setInterval(function() {
        uuid = uuidv4();
    }, 3600000)
module.exports = 
{
    async getTimeline(limit) {
        try {
            let timeline = await axios({
                method: 'get',
                url: `https://${url}/api/v1/timelines/public`,
                data: {
                    limit: limit
                }
            })

            return timeline.data

        } catch(err) {
            throw err
        }
        
    },

    async getNotifications(limit) {
        axios({
            method: 'get',
            url: `https://${url}/api/v1/notifications`,
            headers: { 
                Authorization: `Bearer ${token}`
            },
            data: {
                limit: limit
            }
        }).then(function(notifications){        
            try {
                notifications = notifications.data.filter(function(notif) {
                    return notif.type === "mention"
                })
                notifications = notifications.map(x => x.status)
            } catch(err) {
                console.log("No notifications were found. Continuing...")
            }

            return notifications
        }).catch(function(err) {
            console.log(err.response.data.error)
            fs.appendFile('postodon.log',`${err.response.data.error}\n`, function(err){
                if(err) console.log(err)
                console.log('Wrote to log')
            })
        }) 
    },

    async postStatus(content, mode, visibility, replyToId) {
        if (mode !== 'reply') {
            axios({
                method: 'post',
                url: `https://${url}/api/v1/statuses`,
                headers: { 
                    Authorization: `Bearer ${token}`,
                    Idempotency_Key: uuid
                },
                data: {
                    status: content,
                    visibility: `${visibility}`
                }
            }).then(function(response){
                return response
            }).catch(function(err) {
                console.log(err.response.data.error)
                fs.appendFile('postodon.log',`${err.response.data.error}\n`, function(err){
                    if(err) console.log(err)
                    console.log('Wrote to log')
                })
            })
        } else {
            axios({
                method: 'post',
                url: `https://${url}/api/v1/statuses`,
                headers: { 
                    Authorization: `Bearer ${token}`,
                    Idempotency_Key: uuid
                },
                data: {
                    status: content,
                    in_reply_to_id: replyToId,
                    visibility: `${visibility}`
                }
            }).then(function(response){
                return response
            }).catch(function(err) {
                console.log(err.response.data.error)
                fs.appendFile('postodon.log',`${err.response.data.error}\n`, function(err){
                    if(err) console.log(err)
                    console.log('Wrote to log')
                })
            })

        }
    },
    
    async clearNotifications() {
            axios({
                method: 'post',
                url: `https://${url}/api/v1/notifications/clear`,
                headers: { 
                    Authorization: `Bearer ${token}`
                }
            }).then(function(response){
                return response
            }).catch(function(err) {
                console.log(err.response.data.error)
                fs.appendFile('postodon.log',`${err.response.data.error}\n`, function(err){
                    if(err) console.log(err)
                    console.log('Wrote to log')
                })
                if (err.response.data.error === 'The access token is invalid' || err.response.status === 401) process.exit()
            })
    }   
}