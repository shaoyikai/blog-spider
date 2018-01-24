# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import datetime

class BlogspiderPipeline(object):

    def __init__(self,mysql_host,mysql_port,mysql_user,mysql_password,mysql_database):
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mysql_host=crawler.settings.get('DB_HOST','127.0.0.1'),
            mysql_port=crawler.settings.get('DB_PORT', '3306'),
            mysql_user=crawler.settings.get('DB_USERNAME', 'root'),
            mysql_password=crawler.settings.get('DB_PASSWORD', ''),
            mysql_database=crawler.settings.get('DB_DATABASE', 'test'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            password=self.mysql_password,
            db=self.mysql_database,

            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.db.cursor()
        sql = "INSERT INTO `posts` (`title`,`content`,`created_at`) VALUES (%s,%s,%s)"
        cursor.execute(sql, (item['title'], item['content'], created_at))
        self.db.commit()
        return item
