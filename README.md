# ProacAlert
The objective of this project is to alert users in a timely manner about the new vulnerabilities as per their preference but same time able to run from a Windows desktop machine as a completely local instance. This application get the latest vulnerabilities from NVD NIST data base (https://nvd.nist.gov/vuln/Data-Feeds) by synchronizing every 2 hrs.

Please find the package as a ZIP file,Please extract and configure it in Windows schedule task.

As the synchronization interval is 2 hours there is no need to execute the application before that interval.

The best way to execute this application is via windows schedule task to run every 2 or 3 hrs or once in a day as per your need. 

![alt text](https://s20.postimg.org/fbgml2ykt/sctask1.png)

NB: Please make sure to provide your application directory path in “Start in (Optional)” section otherwise it won’t work.

![alt text](https://s20.postimg.org/oj8v1vst9/sctask2.png)

![alt text](https://s20.postimg.org/m1x3unj7h/sctask3.png)

Alert can be configured via ‘config.ini’ file which comes along with the package. Alert configuration has following sections.

1)Vendor 
2)Product
3)Score

Vendor section let filter the alerts for specific vendors. If you do not want to use this section you can comment out this section by using ; in front of Vendor.

![alt text](https://s20.postimg.org/oxa712csd/conf1.png)

Product section let filter the alerts for specific products. If you do not want to use this section you can comment out this section by using ; in front of Product.

![alt text](https://s20.postimg.org/6uh4a01jx/conf3.png)

Score is the CVE Risk score, by default is 7, you can’t comment out this section but you can tune it between 1 to 10, 1 is  least and 10 is most.

Users can choose Vendor and Product in combination, either one or every alerts based on the score.

If you choose vendor and product same time then it should be a specific match for example, vendor = cisco, juniper and product=ios, junos if you choose vendor = cisco,juniper and product=ios then only cisco and ios based alerts are reported so make sure you configure accordingly.

If you want every alert on particular score then comment out vendor and product section using ; in front of Vendor and Product section. Score is always equal and greater than the value you have provided.

Alerts can be received in 3 ways as follows.

1)Outlool email
2)Email Relay
3)Popup and log (popup is currently tested on Windows7 only)

Outlook let you receive alerts via outlook email, all you need to do is to configure your Outlook and give your email address in the Outlook session of config.ini file as below.

![alt text](https://s20.postimg.org/ldo9bqn2l/conf4.png)

Alerts will be received via email as below.

![alt text](https://s20.postimg.org/mfyfualbh/al1.png)

Email relay let you receive emails via an email relay server, you need to provide sender, receiver, port and IP address of relay server and by removing the ;.The IP address you see in the picture below is a dumy IP so please use your email server IP. If you configure Outlook and Email relay same time then preference will be for email relay.

![alt text](https://s20.postimg.org/f1941e4fh/conf5.png)

If you do not choose neither outlook nor email relay then you will receive the alerts via popup and also a log file will be created in the application directory. Popup is currently tested on Winodws7 only.

![alt text](https://s20.postimg.org/6vr238vm5/al2.png)

This application comes with a sqlite db to avoid duplicate alerting so only new vulnerabilities are reported.

Import Notes.

1)This application required internet connectivity to download data feed from NVD NIST.

2)This application required 7zip command line installed/extracted in C:\Program Files

3)Do not remove any files from the application directory.

4)Make sure to tune properly otherwise you will receive every alerts that can be annoying.



