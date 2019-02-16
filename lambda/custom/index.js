const Alexa = require("alexa-sdk");
const config = require("./configuration");
const eventHandlers = require("./eventHandlers");
const stateHandlers = require("./stateHandlers");
const intentHandlers = require("./intentHandlers");
const speechHandlers = require("./speechHandlers");

exports.handler = function(event, context, callback) {
  let alexa = Alexa.handler(event, context);
  alexa.APP_ID = config.appId;
  alexa.dynamoDBTableName = config.dynamoDBTableName;
  alexa.registerHandlers(
    eventHandlers,
    stateHandlers.startModeIntentHandlers,
    stateHandlers.feedModeIntentHandlers,
    stateHandlers.noNewItemsModeIntentHandlers,
    stateHandlers.singleFeedModeIntentHandlers,
    intentHandlers,
    speechHandlers
  );
  alexa.execute();
};
