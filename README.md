[![Build Status](https://drone.bnolet.me/api/badges/brandon/promptodon/status.svg)](https://drone.bnolet.me/brandon/promptodon)



# promptodon

promptodon is a blog post/journal entry prompt robot that encourages you to write daily.

# Usage

Create a `.env` file in the directory you cloned this repository to containing the variables `ACCESS_TOKEN` and `INSTANCE_URL`.

ACCESS_TOKEN can be found by creating an application at https://YOUR-INSTANCE.EXAMPLE/settings/applications and using the string in the *Your access token* field

INSTANCE_URL is the url at which your bot account/application was created. 

Give the application the following *Scopes*:

```javascript
- read:notifications //check if someone's asked for a prompt
- write:statuses //post at all
- write:notifications // clear notifications on start so replied-to posts aren't replied to again
```

## Node/NPM

Run `npm install` and then `npm run start`

## Docker

You can either start promptodon via docker directly or use the provided docker-compose file. 

### Starting via Docker

docker run --name promptodon bnolet/promptodon --env-file ./env

# Author

This bot was (mostly) created by [linuxliaison](https://fosstodon.org/@brandon). You can either contact him on the Fediverse or via [email](mailto:linuxliaison@fastmail.com). 

# LICENSE

This work was licensed under GPLv3. Check out the [LICENSE](LICENSE) file.