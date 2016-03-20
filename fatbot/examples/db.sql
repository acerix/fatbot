BEGIN TRANSACTION;
CREATE TABLE "trade" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`market_id`	INTEGER NOT NULL,
	`price`	REAL NOT NULL,
	`amount`	INTEGER NOT NULL,
	`trade_id`	INTEGER NOT NULL,
	`trade_time`	INTEGER NOT NULL,
	FOREIGN KEY(`market_id`) REFERENCES `market`(`id`)
);
CREATE TABLE "market" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`exchange_id`	INTEGER NOT NULL,
	`base_currency_id`	INTEGER NOT NULL,
	`trade_currency_id`	INTEGER NOT NULL,
	FOREIGN KEY(`exchange_id`) REFERENCES `exchange`(`id`),
	FOREIGN KEY(`base_currency_id`) REFERENCES `currency`(`id`),
	FOREIGN KEY(`trade_currency_id`) REFERENCES `currency`(`id`)
);
INSERT INTO `market` VALUES (1,1,4,1),
 (2,1,1,3),
 (3,1,1,2);
CREATE TABLE "holding" (
	`id`	INTEGER NOT NULL UNIQUE,
	`exchange_id`	INTEGER NOT NULL,
	`currency_id`	INTEGER NOT NULL,
	`amount`	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY(id),
	FOREIGN KEY(`exchange_id`) REFERENCES `exchange`(`id`),
	FOREIGN KEY(`currency_id`) REFERENCES `currency`(`id`)
);
INSERT INTO `holding` VALUES (1,1,1,0),
 (2,1,2,0),
 (3,1,3,0),
 (4,1,4,0);
CREATE TABLE `exchange` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT NOT NULL UNIQUE
);
INSERT INTO `exchange` VALUES (1,'exmo');
CREATE TABLE "currency" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`code`	TEXT NOT NULL UNIQUE,
	`name`	TEXT NOT NULL UNIQUE,
	`divisor`	INTEGER NOT NULL
);
INSERT INTO `currency` VALUES (1,'BTC','Bitcoin',100000000),
 (2,'LTC','Litecoin',100000000),
 (3,'DOGE','Dogecoin',100000000),
 (4,'USD','US Dollars',100);
COMMIT;
