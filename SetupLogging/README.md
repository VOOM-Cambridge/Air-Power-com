# Setting up Logging:
Run the `setup_logging.sh` script
- Through the terminal: `./setup_logging.sh`
- Through the file manager by double clicking on the `setup_logging.sh` file and selecting run in terminal

## What it does:
- Sets up `rsyslog` to store log files at `/var/log/containers`
- Sets up `logrotate` to limit the number of logs kept to 7 days 
