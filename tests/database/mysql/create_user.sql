CREATE USER 'python'@'%' IDENTIFIED BY 'python';
GRANT ALL PRIVILEGES ON agatereports.* TO 'python'@'%';

FLUSH PRIVILEGES;
