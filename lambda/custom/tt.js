// const jsn = require("./feeds.json");

// console.log(jsn);

const aws = require("aws-sdk");
const s3 = new aws.S3(); // Pass in opts to S3 if necessary
aws.config.update({ region: "us-east-1" });

var params = {
  Bucket: "mhack3",
  Key: "feeds.json"
};
s3.getObject(params, function(err, data) {
  if (err) console.log(err, err.stack);
  // an error occurred
  else {
    let articles = data.Body.toString("utf-8");
    let counts = articles
      .replace(/[^\w\s]/g, "")
      .split(/\s+/)
      .reduce(function(map, word) {
        map[word] = (map[word] || 0) + 1;
        return map;
      }, Object.create(null));
      let c = counts["mmnhji"];
    if (c === undefined) c = 0;
    console.log(c); // successful response
  }
});
