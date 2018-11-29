## DEV WITH DEBIAN
## This script as only be tested on : Debian 9 

import os
import requests

try:
	import MySQLdb
except ModuleNotFoundError:
	os.system("apt install python3-mysqldb -y")
	import MySQLdb

## WORDPRESS VARIABLES
WP_DB_HOST = 'localhost'
WP_DB_NAME = 'wp_database'
WP_DB_USER = 'wp_user'
WP_DB_PASS = 'your_password'

url = input('Enter the URL as \'example.com\' (without \'www\' or \'http(s)\': ')

ssl = input('Do you want an HTTPS website ? (o/n): ').lower() #HTTPS is powered by LetsEncrypt

if ssl != 'o':
	ssl = 'n'

print('MDP WP BDD: ' + WP_DB_PASS)

def install_apache2():
	os.system("apt-get update -y && apt-get upgrade -y && apt-get install apache2 -y")

	os.system("touch /etc/apache2/sites-available/01-{}.conf".format(url))

	vhost_non_conf = open('Ressources/vhost.conf','r')
	vhost_conf = open('/etc/apache2/sites-available/01-{}.conf'.format(url), 'w')

	line = 'not_empty'

	while line:
		line = vhost_non_conf.readline()
		vhost_conf.write(line.format(APACHE_LOG_DIR='{APACHE_LOG_DIR}', votre_url=url))

	vhost_conf.close()

	os.system("mkdir /var/www/html/{}/".format(url))
	os.system("cp /var/www/html/index.html /var/www/html/{}".format(url))
	os.system("a2dissite 000-default")
	os.system("a2ensite 01-{}".format(url))
	os.system("systemctl reload apache2")

	print('Conf Apache OK.')

def install_php():
	os.system("apt-get install php-fpm -y")
	os.system("a2enmod proxy_fcgi setenvif")
	os.system("a2enconf php7.0-fpm")
	os.system("systemctl restart apache2")

	print("Conf PHP OK.")

def install_mysql():
	os.system("apt-get install mysql-server -y && apt-get install php7.0-mysql -y")

	mydb = MySQLdb.connect(host=WP_DB_HOST, user="root", passwd="root")

	mycursor = mydb.cursor()

	mycursor.execute("CREATE DATABASE {};".format(WP_DB_NAME))
	mycursor.execute("CREATE USER \'{}\'@\'{}\' IDENTIFIED BY \'{}\';".format(WP_DB_USER,WP_DB_HOST,WP_DB_PASS))
	mycursor.execute("GRANT ALL PRIVILEGES ON {}.* TO \'{}\'@\'{}\';".format(WP_DB_NAME,WP_DB_USER,WP_DB_HOST))

	print("Conf MySQL OK.")

def install_wp():
	
	os.system("wget https://wordpress.org/latest.tar.gz -P /var/www/html/{}".format(url))
	os.system("tar zxvf /var/www/html/{}/latest.tar.gz -C /var/www/html/{}/".format(url, url))

	secret_key = 'https://api.wordpress.org/secret-key/1.1/salt/'
	r = requests.post(secret_key)

	os.system("touch /var/www/html/{}/wordpress/wp-config.php".format(url))

	wp_non_conf = open('Ressources/wp-config.txt', 'r')
	wp_conf = open('/var/www/html/{}/wordpress/wp-config.php'.format(url), 'w')

	line = 'not_empty'

	while line:
		line = wp_non_conf.readline()
		wp_conf.write(line.format(db_name=WP_DB_NAME,db_user=WP_DB_USER,db_mdp=WP_DB_PASS,key_secret=r.text))

	wp_conf.close()
	
def install_ssl():
	os.system("apt-get install letsencrypt -y")
	os.system("systemctl stop apache2")
	os.system("letsencrypt certonly --standalone --agree-tos --email admin@{site} -d {site} -d www.{site} --standalone-supported-challenges http-01".format(site=url))
	
	vhost_ssl_non_conf = open('Ressources/vhost_ssl.conf','r')
	vhost_ssl_conf = open('/etc/apache2/sites-available/01-{}.conf'.format(url), 'w')

	line = 'not_empty'

	while line:
		line = vhost_ssl_non_conf.readline()
		vhost_ssl_conf.write(line.format(APACHE_LOG_DIR='{APACHE_LOG_DIR}', votre_url=url, HTTPS='{HTTPS}', SERVER_NAME='{SERVER_NAME}', REQUEST_URI='{REQUEST_URI}'))

	vhost_ssl_conf.close()	

	os.system("systemctl start apache2")
	os.system("a2enmod ssl")
	os.system("a2enmod rewrite")
	os.system("systemctl restart apache2")

def auto_renew_ssl():
	#I need to dev it
	print("nothing") 


###Début du PRGM

install_apache2()

if ssl == 'o':
	install_ssl()

install_php()
install_mysql()
install_wp()

print('Please note that this is the password for the wordpress database: ' + WP_DB_PASS)#Display the BDD password. Please note it.