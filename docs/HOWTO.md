# HOW TO

This document is a work in progress but should be enough (if you have a little bit of experience with node or docker) to get you up and running. If you are having issues, feel free to send me a message via [email](mailto:linuxliaison@fastmail.com) or via Mastodon at [@brandon](https://fosstodon.org/@brandon). This document will be further expanded in the future but this, including the repository, is currently being published as a draft to get some feedback.

## env

Create a `.env` file in the directory you cloned this repository to containing the variables `ACCESS_TOKEN`, `INSTANCE_URL`, and `COMMAND`.

ACCESS_TOKEN can be found by creating an application at https://YOUR-INSTANCE.EXAMPLE/settings/applications and using the string in the *Your access token* field

INSTANCE_URL is the url at which your bot account/application was created. 

COMMAND is the command you want your bot to respond to with a random post

REPLY_INTERVAL is the interval at which postodon will check for commands to reply to (in milliseconds)

POST_INTERVAL is the interval at which postodon will post a random status (in milliseconds)

**EXAMPLE .env FILE**

```
ACCESS_TOKEN=3x4mP1et0kEnFR0mY0ur1N574nC3_358nfnslDee
INSTANCE_URL=botinstance.example.com
COMMAND=/yourcommand
REPLY_INTERVAL=5000
POST_INTERVAL=86400000
```

## Permissions

Give the application the following *Scopes*:

```javascript
- read:notifications //check if someone's mentioned you with your slash command
- write:statuses //post at all
- write:notifications // clear notifications on start so replied-to posts aren't replied to again
```


## Adding intros and content

postodon's daily messages are composed of two parts: an intro and content. When postodon creates a post(status), it picks a random intro, a random 'content', and then concatenates them with two newlines in between. 

postodon loads the intros and content by reading the `intros.txt` and `content.txt` files, respectively, and each new line of text is separated into it's own entry of intro or content. To add intros or content to post, just put more text on a new line in one of those files.

Example:


intros.txt

```
This is an intro
This is another intro
This is a third one
```

Above is the intros.txt file. If I wanted to add another intro for postodon to pick from, I just add another intro on another line. 

```
This is an intro
This is another intro
This is a third one
This is a new intro
```

If you want all statuses to have the same intro, simply only include a single one

```
This is what will be posted as an "intro" for every post
```

Same goes with the content.


## Node/NPM

Run `npm install` and then `npm run start`

## Docker

You can either start postodon via docker directly or use the provided docker-compose file. 

### Starting via Docker CLI

docker run --name postodon bnolet/postodon --env-file ./env --volume ./intros.txt:/usr/src/intros.txt --volume ./content.txt:/usr/src/content.txt
