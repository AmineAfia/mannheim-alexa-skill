const nodemailer = require("nodemailer");
const aws = require("aws-sdk");
aws.config.update({ region: "us-east-1" });
const ses = new aws.SES();
const params = {
  Destination: {
    BccAddresses: [],
    CcAddresses: ["afia.amine@gmail.com"],
    ToAddresses: ["afia.amine@gmail.com"]
  },
  Message: {
    Body: {
      Html: {
        Charset: "UTF-8",
        Data:
          'This message body contains HTML formatting. It can, for example, contain links like this one: <a class="ulink" href="http://docs.aws.amazon.com/ses/latest/DeveloperGuide" target="_blank">Amazon SES Developer Guide</a>.'
      },
      Text: {
        Charset: "UTF-8",
        Data: "This is the message body in text format."
      }
    },
    Subject: {
      Charset: "UTF-8",
      Data: "Test email 1"
    }
  },
  ReplyToAddresses: [],
  Source: "mealsanddeals4u@gmail.com",
  SourceArn:
    "arn:aws:ses:us-east-1:603584112335:identity/mealsanddeals4u@gmail.com"
};

const mailSender = function() {
  // const transporter = nodemailer.createTransport({
  //   service: "gmail",
  //   auth: {
  //     user: "mealsanddeals4u@gmail.com",
  //     pass: "Meals&Deals4u"
  //   }
  // });

  return {
    sendEmail: ses.sendEmail(params, function(err, data) {
      if (err) console.log(err, err.stack);
      // an error occurred
      else console.log(data); // successful response
      /*
     data = {
      MessageId: "EXAMPLE78603177f-7a5433e7-8edb-42ae-af10-f0181f34d6ee-000000"
     }
     */
    })
  };

  // console.log("Creating SES transporter");
  // // create Nodemailer SES transporter
  // const transporter = nodemailer.createTransport({
  //   SES: ses
  // });

  // const mailOptions = {
  //   from: "mealsanddeals4u@gmail.com",
  //   to: "afia.amine@gmail.com",
  //   subject: "Dope E-Mail from mannheim skill",
  //   text: "Mailing you from Mannheim Skill 1"
  // };

  // transporter.sendMail(mailOptions, function(error, info) {
  //   if (error) {
  //     console.log(error);
  //   } else {
  //     console.log("Email sent: " + info.response);
  //   }
  // });
};

module.exports = mailSender;
