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
        Data: "<html><head> <title>Your Digest</title> </head> <body> <div id='rectangle' style='width: 90%; height: 100px; background-color: #ADC3E5'> <h2> <center>Ads goes here</center> <center></center> </h2> </div><div style='width: 90%; background-color: #E1E1E1'> <br><h2><center>Your digest</center></h2> <ul> <li><a href='test'>Alles dreht sich ums Hacken im Mafinex.</a></li><li><a href='test'>Mannheim: Schrotthändler überfallen und verletzt - Polizei stoppt Verdächtige in zwei Lastwagen</a></li><li><a href='test'>Kunstraub sorgt für Spannung und Heiterkeit </a></li><li><a href='https://www.morgenweb.de/mannheimer-morgen_artikel,-mannheim-sparkasse-eigenes-cafe-_arid,1402308.html'>Sparkasse: eigenes Café</a></li></ul> <br></div><div id='rectangle' style='width: 90%; height: 100px; background-color: #ADC3E5'> <h2> <center>Ads goes here</center> </h2> </div></body></html>"
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
