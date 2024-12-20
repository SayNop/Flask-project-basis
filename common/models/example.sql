SET @@auto_increment_increment=9;

-- CREATE DATABASE IF NOT EXISTS example;
-- mysql -uroot -p -Dexample < example.sql

DROP TABLE IF EXISTS `login_user`;
CREATE TABLE `login_user` (
    `phone` char(11) NOT NULL COMMENT 'phone number',
    `username` varchar(15) NOT NULL COMMENT 'nickname',
    `password` varchar (120) NOT NULL COMMENT 'password',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'create time',
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'update time',
    `last_login` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'last login time',
    PRIMARY KEY (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Login User';
