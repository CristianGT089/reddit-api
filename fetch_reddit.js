import snoowrap from 'snoowrap';

const reddit = new snoowrap({
    userAgent: 'Cristian-Analisis/1.0',
    clientId: 'heb2VXcSiegulvbOO-Y5-w',
    clientSecret: '_uzEu15A-Zr1bbFbS-EorDhrOE24vA',
    username: 'UnoMas_UnoMenos',
    password: 'HelloWorld0809',
});

const subreddit = process.argv[2];
const limit = parseInt(process.argv[3]);

reddit.getSubreddit(subreddit).getHot({ limit }).then(posts => {
    const titles = posts.map(post => post.title);
    console.log(JSON.stringify(titles));
}).catch(error => {
    console.error(error);
    process.exit(1);
});
