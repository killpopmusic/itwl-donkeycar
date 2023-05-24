# DONKEYCAR_SETUP_TROUBLESHOOTING

To set up the car the steps from official docummentation https://docs.donkeycar.com/guide/install_software/ were followed, below there are listed solutions 
to the issues that occurred during the process

## SSH conncetion 

If errors occure during the connection process make sure the RPI's OS is up to date. In RPI's terminal enter:


```bash
sudo apt update
sudo apt upgrade
```
Check if SSH is active 
``bash
sudo service ssh status
```




