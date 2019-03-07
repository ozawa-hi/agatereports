CREATE TABLE `agatereports`.`tasks` (
  `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `series` VARCHAR(45) NOT NULL,
  `task` VARCHAR(45) NULL,
  `subtask` VARCHAR(45) NULL,
  `starttimestamp` TIMESTAMP NULL,
  `endtimestamp` TIMESTAMP NULL,
  `percent` DECIMAL(10,2) NULL);

INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Scheduled','task1','subtask1','1998-05-06 00:00:00.000000000','1998-05-07 00:00:00.000000000',NULL);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Scheduled','task1','subtask2','1998-05-01 00:00:00.000000000','1998-05-02 00:00:00.000000000',NULL);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Scheduled','task1','subtask3','1998-05-03 00:00:00.000000000','1998-05-05 00:00:00.000000000',NULL);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Scheduled','task1','subtask4','1998-05-11 00:00:00.000000000','1998-05-15 00:00:00.000000000',NULL);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Scheduled','task2','subtask1','1998-05-06 00:00:00.000000000','1998-05-08 00:00:00.000000000',NULL);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Scheduled','task2','subtask2','1998-05-08 06:00:00.000000000','1998-05-09 00:00:00.000000000',NULL);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Scheduled','task2','subtask3','1998-05-10 00:00:00.000000000','1998-05-15 00:00:00.000000000',NULL);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Scheduled','task3','subtask1','1998-05-07 00:00:00.000000000','1998-05-08 00:00:00.000000000',NULL);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Actual','task1','subtask1','1998-05-07 00:00:00.000000000','1998-05-09 00:00:00.000000000',0.25);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Actual','task1','subtask2','1998-05-01 00:00:00.000000000','1998-05-02 00:00:00.000000000',0.85);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Actual','task1','subtask3','1998-05-02 00:00:00.000000000','1998-05-05 00:00:00.000000000',0.50);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Actual','task1','subtask4','1998-05-12 00:00:00.000000000','1998-05-15 00:00:00.000000000',1.00);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Actual','task2','subtask1','1998-05-06 00:00:00.000000000','1998-05-10 00:00:00.000000000',0.15);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Actual','task2','subtask2','1998-05-18 06:00:00.000000000','1998-05-19 00:00:00.000000000',0.20);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Actual','task2','subtask3','1998-05-11 00:00:00.000000000','1998-05-15 00:00:00.000000000',0.45);
INSERT INTO `agatereports`.`tasks` (series,task,subtask,starttimestamp,endtimestamp,percent) VALUES('Actual','task3','subtask1','1998-05-10 00:00:00.000000000','1998-05-11 00:00:00.000000000',0.95);
