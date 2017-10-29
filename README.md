# ProacAlert
The aim of this project is to alert users in a timely manner about the new vulnerabilities as per their preferences.

The advantages of this application are:

1)This application can run from a Windows desktop.

2)Easily filter based on Vendor, Product and CVE risk score.

3)No need to publish email or IP address in external sites to receive alerts.


Prerequisites for this application are:

1) Internet connectivity

2) Command line version of 7-Zip program in either C:\ or C:\Program Files.

How does it works?

This application gets the latest vulnerabilities from NVD NIST data base (https://nvd.nist.gov/vuln/Data-Feeds). By default synchronizing interval is every 2 hours but you can tune it the way you want via Windows schedule task.

NB: As the synchronization interval is 2 hours there is no need to execute the application before that interval.

How to install this application?

1) Please download the ProacAlert.7z, extract it in a folder.

2) Open config.ini file and filter based on your preference.

3) Test it by executing ProacAlert.exe.

4) Configure it via Windows schedule task to receive alerts regularly

How to configure/filter the alerts?

Alerts can be configured via ‘config.ini’ file which comes along with the package. Alerts configuration has following sections:

1)Vendor

2)Product

3)Score

Vendor section let filter the alerts for specific vendors.You can add or remove vendors from the config.ini as per your preference. If you do not want to use this section you can comment out this section by using ; in front of Vendor.

![alt text](https://s20.postimg.org/82x6q8bjh/conf6.png)

Product section let filter the alerts for specific products.You can add or remove products from the config.ini as per your preference. If you do not want to use this section you can comment out this section by using ; in front of Product.

![alt text](https://s20.postimg.org/6nvm1mkrx/conf7.png)

Score is the CVE Risk score, by default is 7, you cannot comment out this section but you can tune it between 1 to 10, 1 is least and 10 is most.

Users can choose Vendor and Product in combination, either one or every alert based on the score.

If you choose vendor and product same time then it should be a specific match for example, vendor = cisco, juniper and product=ios, junos if you choose vendor = cisco,juniper and product=ios then only cisco and ios based alerts are reported so make sure you configure accordingly.

If you want every alert on particular score then comment out vendor and product section using ; in front of Vendor and Product section. Score is always equal and greater than the value you have provided.

How to receive alerts?

Alerts can be received in 3 ways as follows.

1)Outlool email

2)Email Relay

3)Popup and log (popup is currently tested on Windows7 only)

Outlook let you receive alerts via outlook email, all you need to do is to configure your Outlook and give your email address in the Outlook session of config.ini file as below.(The email in the screen shot is a dummy one, please change it to your email address)

![alt text](https://s20.postimg.org/f339jsb4d/outlook.png)

Alerts will be received via email as below.

![alt text](https://s20.postimg.org/mfyfualbh/al1.png)

Email relay let you receive emails via an email relay server, you need to provide sender, receiver, port and IP address of relay server and by removing the ;.The IP address you see in the picture below is a dumy IP so please use your email server IP. If you configure Outlook and Email relay same time then preference will be for email relay.

![alt text](https://s20.postimg.org/q2ogv8wct/emailrelay.png)

If you do not choose neither outlook nor email relay then you will receive the alerts via popup (Popup only for Windows7) and also a log file will be created in the application directory. 

![alt text](https://s20.postimg.org/6vr238vm5/al2.png)

This application comes with a sqlite db to avoid duplicate alerting so only new vulnerabilities are reported.

NB: The best way to receive the alerts is via Outlook. 


The best way to execute this application is via windows schedule task to run every 2 or 3 hours or once in a day as per your need. 

![alt text](https://s20.postimg.org/fbgml2ykt/sctask1.png)

NB: Please make sure to provide your application directory path in “Start in (Optional)” section otherwise it will not work.

![alt text](https://s20.postimg.org/oj8v1vst9/sctask2.png)

![alt text](https://s20.postimg.org/m1x3unj7h/sctask3.png)

Important Notes.

1)This application requires internet connectivity to download data feed from NVD NIST.

2)This application requires 7zip command line installed/extracted in C:\Program Files

3)Do not remove any files from the application directory.

4)Make sure to tune properly otherwise you will receive every alert, which can be annoying.


Please reach me out via my email sreeju_kc@hotmail.com if you have any queries.
