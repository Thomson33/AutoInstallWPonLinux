# AutoInstallWPonLinux
Python script to automatically install Wordpress in Debian 9

## Prepare your setup

To use this script you need to install Python3 and pip3.
On debian : `apt-get install python3 pip3`

After install Python3 and pip3, please install theses librairies : `MySQLdb` and `requests`. (`pip3 install requests` and `apt install python3-mysqldb -y` on your command line)

## Run the script

When that was done, you have to edit the script `program.py` with your own informations.

Finally you can run the script by using : `python3 program.py`. Run the script in **root** user !

## Informations

This script has only be tested on Debian 9 ! 

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
