# DONKEYCAR_SETUP_TROUBLESHOOTING

To set up the car the steps from official docummentation https://docs.donkeycar.com/guide/install_software/ were followed, below there are listed solutions 
to the issues that occurred during the process

The name of the user has been set to ****piracer****, make sure to keep that in mind while following the official instruction

## SSH conncetion 


If errors occure during the connection process make sure the RPI's OS is up to date. In RPI's terminal enter:


```bash
sudo apt update
sudo apt upgrade
```
Check if SSH is active 

```bash
sudo service ssh status
```
If the status is not active, start it: 

```bash
sudo service ssh start
```
In case you still can't SSH into the vehicle you may try changing SSH server configuration file:

```bash
sudo nano /etc/ssh/sshd_config
```

Look for the line that says ****PasswordAuthentication**** and ensure it is set to ****yes****. If it is set to no, change it and save the file.

Restart the SSH service
```bash
sudo service ssh restart
```



