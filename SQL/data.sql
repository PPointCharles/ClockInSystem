create database if not exists `flask`;
use flask;
create table if not exists `user`(
    `id` int unsigned auto_increment,
    `username` varchar(20) not null,
    `password` varchar(40) not null,
    primary key ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists `record`(
    `id` int unsigned auto_increment,
    `user_id` int unsigned not null,
    `time` DATETIME not null,
    primary key ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists `summary`(
    `id` int unsigned auto_increment,
    `user_id` int unsigned not null,
    `year` int not null,
    `month` int not null,
    `day` int not null,
    `duration` float not null,
    primary key ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into `user` values
(1, 'HB', '123456'),
(2, 'DB', '123456'),
(3, 'GB', '123456'),
(4, 'LB', '123456');

-- insert into record(user_id, time) values(2, '2021-04-10 11:51:00');
