const axios = require('axios').default
const uuidv4 = require('uuid').v4
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
        let notifications = await axios({
            method: 'get',
            url: `https://${url}/api/v1/notifications`,
            headers: { 
                Authorization: `Bearer ${token}`
            },
            data: {
                limit: limit
            }
        })
        
        try {
            notifications = notifications.data.filter(function(notif) {
                return notif.type === "mention"
            })
            notifications = notifications.map(x => x.status)
        } catch(err) {
            console.log("No notifications were found. Continuing...")
        }

        
        return notifications
        
        
    },

    async postStatus(content, mode, visibility, replyToId) {
        if (mode !== 'reply') {
            try {
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
                })
            } catch(err) {
                throw err
            }
        } else {
            try {
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
                })
            } catch(err) {
                throw err
            }
        }
    } 
}