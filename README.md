# Bestbuy-Scalper
The Bestbuy scalper is a simple Python script that removes the stresses of waiting for a product to go on sale. Although it's still in development and extensive bug testing, its goal is to use a provided link to a BestBuy product and check every second until it sees it go for sale. For instance, an Nvidia 3080 gpu. Once it's done inputting your account information, it will then add the item to your cart and continue to the checkout so it can have the sweet 15-minute reservation. After all this, it will then send you a message to a provided phone number or email to let your know that your item is ready.

# Installation
To run this script, when you install it, you need to install a Chrome Driver - https://chromedriver.chromium.org/ - and add it to the main directory of the script.

# Setup
To allow this to run, you need to create a throw away email as some people call it. Google gmail allows your to create emails for free. Its called a throw away email becasue you dont care what happens to it, this is becasuse you need to disable all authentication on the account to let the bot can login. Instead of paying for twilio, I used a module called smtplib to send emails, this is becasue a phone number can be altered into an email. For instance, AT&T is phonenumber@mms.att.net. When you create this email, you will want to set its email and password on line 40 and 41. This hasnt been tested for any other email except Gmail.

Use PIP to install all the modules
