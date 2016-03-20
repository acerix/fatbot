BEGIN TRANSACTION;
CREATE TABLE "symbol" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`code`	TEXT NOT NULL UNIQUE,
	`name`	TEXT NOT NULL UNIQUE
);
INSERT INTO `symbol` VALUES (1,'BTC','Bitcoin'),
 (2,'LTC','Litecoin'),
 (3,'DOGE','Dogecoin');
CREATE TABLE "holding" (
	`id`	INTEGER NOT NULL UNIQUE,
	`exchange_id`	INTEGER NOT NULL,
	`symbol_id`	INTEGER NOT NULL,
	`amount`	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY(id),
	FOREIGN KEY(`exchange_id`) REFERENCES `exchange`(`id`),
	FOREIGN KEY(`symbol_id`) REFERENCES `symbol`(`id`)
);
CREATE TABLE `exchange` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT NOT NULL UNIQUE
);
INSERT INTO `exchange` VALUES (1,'exmo');
COMMIT;
