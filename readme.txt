# title           :miscron.py
# description     : Runs commands to a server
# author          :Chris Sprance / Entrada Interactive
# usage           : This script is CLI for server administaration to run it from a command line do:
# misrcon.py -i [ip] --port [admin port] -p [admin password] --command [command] --time [exec_time] --s [schedule]
# python_version  :2.7.5


To run this program you must have Python 2.7 installed on your machine somewhere.

navigate to where you extracted the script and run 
python misrcon.py --help to get instruction on what is required to send or schedule a command

a typical command would look like

python misrcon.py -i 192.168.1.1 --port 40565 -p password --command sv_say "The server will be restarting soon" --time 12:45 --s
This command would schedule only a connection to the server 192.168.1.1:40565 using the password password and then send the command sv_say The server will be restarting soon at 12:45 tomorrow and keep the window open until it executes tomorrow and then it will reschedule itself to run again +1 day

python misrcon.py -i 192.168.1.1 --port 40565 -p password --command sv_say "You're all noobs"
This command would make a connection to the server 192.168.1.1:40565 using the password password and then send the command sv_say You're all noobs

python misrcon.py -i 192.168.1.1 --port 40565 -p password --command sv_say "You're all noobs" --time 12:45
This command would make a connection to the server 192.168.1.1:40565 using the password password and then send the command sv_say You're all noobs and then schedule that same command to run again tomorrow at 12:45