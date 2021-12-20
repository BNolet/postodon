const axios = require('axios').default
const uuidv4 = require('uuid').v4
const { Console } = require('console')
const fs = require('fs')
const url = process.env.INSTANCE_URL
const token = process.env.ACCESS_TOKEN
let uuid = uuidv4()
setInterval(function() {
        uuid = uuidv4();
    }, 3600000)


function errorLogger(error) {
    let errorcontents
    switch(error.response.status) {
        case 401:
            errorcontents = `${new Date} - The access token is invalid\n`
            break
        case 403:
            errorcontents = `${new Date} - You need - read:notifications, write:statuses, and write:notifications permissions. See https://github.com/BNolet/postodon/blob/master/docs/HOWTO.md for more info.\n`
    }
    fs.appendFile('postodon.log',errorcontents, function(err){
        if(err) console.log(err)
        console.log(errorcontents)
        if (error.response.status === 403 || error.response.status === 401) process.exit()
    })
}
module.exports = 
{
    async getTimeline(limit) {
        axios({
            method: 'get',
            url: `https://${url}/api/v1/timelines/public`,
            data: {
                limit: limit
            }
        }).then(timeline => {
            console.log(timeline)
            return timeline.data
        }).catch(err => errorLogger(err))
        
    },

    async getNotifications(limit) {
        return axios({
            method: 'get',
            url: `https://${url}/api/v1/notifications`,
            headers: { 
                Authorization: `Bearer ${token}`
            },
            data: {
                limit: limit
            }
        }).then(response => {        
            response = response.data.filter(function(notif) {
                return notif.type === "mention"
            })
            response = response.map(x => x.status)
            return response
        }).catch(err => errorLogger(err))
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
            }).catch(err => errorLogger(err))
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
            }).catch(err => errorLogger(err))

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
            }).catch(err => errorLogger(err))
    },

    
}