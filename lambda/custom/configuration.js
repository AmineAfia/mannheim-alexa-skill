let config = {
  // TODO Add Application ID
  appId: "amzn1.ask.skill.c7458e75-997a-443d-9f7e-302bfb5ab862",
  // TODO Add an appropriate welcome message.
  welcome_message: "Wilkommen bei Mannheim. Eine Skill von Mannheimer Morgen. ",

  number_feeds_per_prompt: 3,
  speak_only_feed_title: true,
  display_only_title_in_card: true,

  // TODO Add the category name (to feed name) and the corresponding URL
  feeds: {
    // Muddassir: "https://rss.nytimes.com/services/xml/rss/nyt/Europe.xml",
    news: "https://www.morgenweb.de/feed/201-alexa-advanced-mm-startseite.xml"
    // Muddassir1:
    //   "https://xmedias2.morgenweb.de/feed/201-alexa-advanced-mm-startseite.xml"
    // CATEGORY_NAME_2: "<FEED_URL>",
    // CATEGORY_NAME_3: "<FEED_URL>"
  },

  speech_style_for_numbering_feeds: "Item",

  // TODO Add the s3 Bucket Name, dynamoDB Table Name and Region
  s3BucketName: "mhack3",
  dynamoDBTableName: "MannheimTable",
  dynamoDBRegion: "us-east-1"
};

module.exports = config;
