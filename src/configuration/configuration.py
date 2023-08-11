import os

class DevelopmentConfig():
    DEBUG=True
    PORT=3000
    HOST="0.0.0.0"
    MYSQL_HOST="blmod5qijpypbdkulgkx-mysql.services.clever-cloud.com"
    MYSQL_USER = "uiw2jpozbyviv3zo"
    MYSQL_PASSWORD = "4KtI2wh5vAEQade0mKjx"
    MYSQL_DB = "blmod5qijpypbdkulgkx"

configuracion={
    'development':DevelopmentConfig
}