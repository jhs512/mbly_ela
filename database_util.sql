# MariaDB sbsst 사용자 생성
GRANT ALL PRIVILEGES ON *.* TO sbsst@`%` IDENTIFIED BY 'sbs123414';

# DB 초기화
DROP DATABASE IF EXISTS sample1_dev;
CREATE DATABASE sample1_dev;
USE sample1_dev;
