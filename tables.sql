CREATE DATABASE   mafengwo ;
USE mafengwo
	CREATE  TABLE   personalUrl
	(
		uid VARCHAR(30) Primary Key,
		perUrl VARCHAR(50)
	);
	CREATE  TABLE  tourist
	(
    uid VARCHAR(30) Primary Key,
    uname VARCHAR(20) CHARACTER SET 'utf8',
    gender ENUM('female','male'),
    residence VARCHAR(15) CHARACTER SET 'utf8',
		lng DOUBLE(16,10),
		lat DOUBLE(16,10)
	);
	CREATE  TABLE  travelNote
	(
		nid VARCHAR(30) Primary Key,
		uid VARCHAR(30),
		travelDate DATE,
		travelDays INT,
		travelCost DOUBLE(9,3),
		spot VARCHAR(20) CHARACTER SET 'utf8',
		lng DOUBLE(16,10),
		lat DOUBLE(16,10),
		foreign key (uid) references tourist(uid)
	);
