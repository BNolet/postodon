module.exports = {
    getRandomPrompt() {
        let intros = [
            'Good morning/night :), does this make you want to write?\n\n',
            'Hey there, try writing about this:\n\n',
            'Here\'s a journal prompt for you!\n\n',
            'What about writing something like this today?\n\n',
            'There\'s a lot of things you could write about today, maybe this one?\n\n',
            'A new day, a new entry. Write something along the lines of this\n\n',
            'Feeling bored? You could try contemplating this and writing about it\n\n'
        ]
        let random1 = intros[Math.floor(Math.random() * intros.length)]
        let prompts = [
            `${random1}What are your goals for this month?`,
            `${random1}Is this season affecting you in some way?`,
            `${random1}What would your dream garden look like?`,
            `${random1}How would you like to spend your next rainy day?`,
            `${random1}Who do you look up to and why?`,
            `${random1}What kind of clutter do you have in your life that you'd like to get rid of?`,
            `${random1}Do you think you could make money selling things you don't use in your home?`,
            `${random1}How would you best take advantage of a rainy day?`,
            `${random1}Are you reaching your monthly goals?`,
            `${random1}Write about your last vacation.`,
            `${random1}If money wasn't an object, what would you study in school?`,
            `${random1}What are you looking forward to?`,
            `${random1}Write a poem about this season.`,
            `${random1}What do you plan to do next long weekend?`,
            `${random1}Tell the fictional story of a vacation you went on last summer. Make something up :)`,
            `${random1}What do you want to get done before the day/month/year is over?`,
            `${random1}What's your favourite activity of the season?`,
            `${random1}If you could vacation around the world for a year, who would you do it with an why?`,
            `${random1}Write about something new you did recently.`
        ]
        const random2 = Math.floor(Math.random() * prompts.length)
        return prompts[random2]
    }
}