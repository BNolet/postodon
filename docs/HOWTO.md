# HOW TO

This document is a work in progress but should be enough (if you have a little bit of experience with node or docker) to get you up and running. If you are having issues, feel free to send me a message via [email](mailto:linuxliaison@fastmail.com) or via Mastodon at [@brandon](https://fosstodon.org/@brandon). This document will be further expanded in the future but this, including the repository, is currently being published as a draft to get some feedback.

## env

Create a `.env` file in the directory you cloned this repository to containing the variables `ACCESS_TOKEN`, `INSTANCE_URL`, and `COMMAND`.

ACCESS_TOKEN can be found by creating an application at https://YOUR-INSTANCE.EXAMPLE/settings/applications and using the string in the *Your access token* field

INSTANCE_URL is the url at which your bot account/application was created. 

COMMAND is the command you want your bot to respond to with a random post

**EXAMPLE .env FILE**

```
ACCESS_TOKEN=3x4mP1et0kEnFR0mY0ur1N574nC3_358nfnslDee
INSTANCE_URL=botinstance.example.com
COMMAND=/yourcommand
```

## Permissions

Give the application the following *Scopes*:

```javascript
- read:notifications //check if someone's mentioned you with your slash command
- write:statuses //post at all
- write:notifications // clear notifications on start so replied-to posts aren't replied to again
```

## Node/NPM

Run `npm install` and then `npm run start`

## Docker

You can either start postodon via docker directly or use the provided docker-compose file. 

### Starting via Docker CLI

docker run --name postodon bnolet/postodon --env-file ./env
