"""

Install and configure Wordpress on an Debian 9 machine
Used Apache2, PHP 7.0, MySQL and Let's encrypt (SSL is optionnal)
Only be tested on Debian 9

"""

import os

from variables import *
from functions import *

#Beginning of the program
url = input('Enter the URL as \'example.com\' (without \'www\' or \'http(s)\': ')

ssl = input('Do you want an HTTPS website ? (o/n): ').lower() #HTTPS is powered by LetsEncrypt

install_apache2(url)

if ssl == 'o':
	install_ssl(url)

install_php()
install_mysql()
install_wp(url)

print('Installation finished !')