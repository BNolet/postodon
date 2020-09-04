
# postodon

Postodon is a server that will post to mastodon at a given interval, with each post consisting of an intro and content. This project was forked from [promptodon](https://bitea.bnolet.me/brandon/promptodon) as I saw the use of a more general purpose interval-based posting bot. 

# Usage

You can either run the bot raw using node or run it in a docker container using the provided docker-compose.yml file. If you find any issues with that file, feel free to open an issue. See [HOWTO.md](docs/HOWTO.md) for more usage info.

# The basics

Postodon will post to a designated mastodon account on a daily basis by default. It does this by taking an intro (taken from a single line in the intros.txt file you provide) and a piece of content (taken from a single line in the content.txt file you provide) and concatenates the two together, separated by a single empty line, and sends a POST request to the designated server. The account on that server to which the access token belongs to will be the account you post to. You must create the access token beforehand or else your bot will not know which account to post to. 

# WARNING

This bot is being published as a work in progress and I am actively seeking feedback on various things such as error handling, clarity of documentation, and ease of use. Feel free to open an issue, contact me via [email](mailto:linuxliaison@fastmail.com), or via Mastodon [@brandon@fosstodon.org](https://fosstodon.org/@brandon). This bot has very little to no error handling at this point. The code is provided as is for the moment, but I will be taking feature requests. 

# Author

This bot was (mostly) created by [linuxliaison](https://fosstodon.org/@brandon). You can either contact him on the Fediverse or via [email](mailto:linuxliaison@fastmail.com). 

# LICENSE

This work is licensed under GPLv3. Check out the [LICENSE](LICENSE) file.
