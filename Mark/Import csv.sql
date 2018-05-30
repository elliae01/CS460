Insert into sysman.SHOOTER_TABLE (S_INDEX,S_DATE,S_SHOOTER) values (2561,to_timestamp('09-FEB-28 05.47.08.976123456 PM','DD-MON-RR HH.MI.SSXFF AM'),SYSMAN.SHOOTER(99,SYSMAN.LOC_OBJ(125,68,25),0,0,156,SYSMAN.ARM_OBJ(SYSMAN.EMG_OBJ(732947205473264178),1999,99996,-7341),0,SYSMAN.ORIENT_OBJ(131.5625,-99,-99),SYSMAN.ORIENT_OBJ(131.5625,0.3125,-71.8125)))

Insert into SHOOTER_TABLE (S_INDEX,S_DATE,S_SHOOTER) values
(2567,
to_timestamp('09-FEB-28 05.47.08.976123456 PM','DD-MON-RR HH.MI.SSXFF AM'),
SYSMAN.SHOOTER(
99,
SYSMAN.LOC_OBJ(1,2,3),
99,
99,
99,
SYSMAN.ARM_OBJ(SYSMAN.EMG_OBJ(7,3,2,9,4,7,2,0),99,99,99),
99,
SYSMAN.ORIENT_OBJ(100.100,-99,-99),
SYSMAN.ORIENT_OBJ(100.100,-100,-100)
)
)

DROP TABLE Shooter_Table;
DROP TABLE Target_Table;
DROP TYPE TARGET;
DROP TYPE SHOOTER;
DROP TYPE ENTITY;
DROP TYPE Arm_Obj;
DROP TYPE Emg_Obj;
DROP TYPE Orient_Obj;
DROP TYPE Loc_Obj;



CREATE TYPE Loc_Obj AS OBJECT
(x NUMBER, y NUMBER, z NUMBER);

CREATE TYPE Orient_Obj AS OBJECT
(heading FLOAT, roll FLOAT, pitch FLOAT);

CREATE TYPE Emg_Obj AS OBJECT
(emg0 NUMBER, emg1 NUMBER, emg2 NUMBER, emg3 NUMBER, emg4 NUMBER, emg5 NUMBER, emg6 NUMBER, emg7 NUMBER);

CREATE TYPE Arm_Obj AS OBJECT
(emg Emg_Obj, roll FLOAT, pitch FLOAT, heading FLOAT);

CREATE TYPE ENTITY AS OBJECT
(id NUMBER, loc Loc_Obj, hostility NUMBER, hit NUMBER) NOT FINAL;

CREATE TYPE SHOOTER UNDER ENTITY
(hr NUMBER, arm Arm_Obj, shot NUMBER, body Orient_Obj, head Orient_Obj) NOT FINAL;

CREATE TYPE TARGET UNDER ENTITY
(visible NUMBER);



CREATE TABLE Target_Table
(t_index NUMBER NOT NULL, t_date TIMESTAMP, t_target Target,
CONSTRAINT target_PK PRIMARY KEY(t_index));

CREATE SEQUENCE target_index_seq
  START WITH 1
  INCREMENT BY 1;
  
  
  
CREATE TABLE Shooter_Table
(s_index NUMBER NOT NULL, s_date TIMESTAMP, s_shooter SHOOTER,
CONSTRAINT shooter_PK PRIMARY KEY(s_index));

CREATE SEQUENCE shooter_index_seq
  START WITH 1
  INCREMENT BY 1;






--me
DROP TABLE Target_Table;
DROP TABLE Shooter_Table;
--Drop TABLE Emg_Table;
--drop TABLE Emg
Drop SEQUENCE shooter_index_seq
Drop SEQUENCE Target_index_seq
DROP TYPE Arm_Obj
DROP TYPE ENTITY
DROP TYPE ORIENT_OBJ
DROP TYPE Loc_Obj
DROP TYPE Emg_Obj
DROP TYPE SHOOTER
DROP TYPE TARGET


CREATE TYPE Emg_Obj AS object
(emg0 FLOAT, emg1 FLOAT, emg2 FLOAT, emg3 FLOAT, emg4 FLOAT, emg5 FLOAT, emg6 FLOAT, emg7 FLOAT)

CREATE TYPE Arm_Obj AS OBJECT
(emg Emg_Obj, roll FLOAT, pitch FLOAT, heading FLOAT)

CREATE TYPE Orient_Obj AS OBJECT
(heading FLOAT, roll FLOAT, pitch FLOAT)

CREATE TYPE Loc_Obj AS OBJECT
(x NUMBER, y NUMBER, z NUMBER)

CREATE TYPE ENTITY AS OBJECT
(id NUMBER, loc Loc_Obj, hostility NUMBER, hit NUMBER) NOT FINAL;

CREATE TYPE SHOOTER UNDER ENTITY
(hr NUMBER, arm Arm_Obj, shot NUMBER, body Orient_Obj, head Orient_Obj) NOT FINAL;

CREATE TYPE TARGET UNDER ENTITY
(visible NUMBER)

--CREATE TYPE Emg_Obj AS VARRAY(10) OF NUMBER
CREATE SEQUENCE target_index_seq
  START WITH 1
  INCREMENT BY 1

CREATE SEQUENCE shooter_index_seq
  START WITH 1
  INCREMENT BY 1


CREATE TABLE Target_Table(
 t_index NUMBER NOT NULL,
 t_date TIMESTAMP,
 t_target Target,
 CONSTRAINT target_PK PRIMARY KEY(t_index))



CREATE TABLE Shooter_Table
(s_index NUMBER NOT NULL, s_date TIMESTAMP, s_shooter SHOOTER,
CONSTRAINT shooter_PK PRIMARY KEY(s_index))


--CREATE TABLE Emg
--(e_index Number, e_emg Emg_obj,
--CONSTRAINT Emg_PK PRIMARY KEY(e_index))

INSERT INTO Target_Table
VALUES(
target_index_seq.nextval,
CURRENT_TIMESTAMP,
Target(1,Loc_Obj(2,3,4),5,6,7))

SELECT *
FROM Target_Table t

INSERT INTO Shooter_Table
VALUES(
shooter_index_seq.nextval,
CURRENT_TIMESTAMP,
SHOOTER(
1,
Loc_Obj(21,61,78),
2,
3,
4,
Arm_Obj(Emg_Obj(1,2,3,4,5,6,7,8),23.2,31.5,87.3),
5,
Orient_Obj(32.4,57.3,27.2),
Orient_Obj(21.4,77.3,29.2))
)

DECLARE
    EmgData arm.emg;
BEGIN
Select s.S_INDEX,s.S_DATE,
s.S_SHOOTER.Id,
s.S_SHOOTER.Loc.x,
s.S_SHOOTER.Loc.y,
s.S_SHOOTER.Loc.z,
s.S_SHOOTER.hostility,
s.S_SHOOTER.hit,
s.S_SHOOTER.hr,
s.S_SHOOTER.arm.emg.Emg_obj(1),
s.S_SHOOTER.arm.roll,
s.S_SHOOTER.arm.pitch,
s.S_SHOOTER.arm.heading,
s.S_SHOOTER.shot,
s.S_SHOOTER.body.heading,
s.S_SHOOTER.body.roll,
s.S_SHOOTER.body.pitch,
s.S_SHOOTER.head.heading,
s.S_SHOOTER.head.roll,
s.S_SHOOTER.head.pitch
FROM Shooter_Table s
END;

Select s.S_INDEX,s.S_DATE,s.S_SHOOTER.Id,s.S_SHOOTER.Loc.x,s.S_SHOOTER.Loc.y,s.S_SHOOTER.Loc.z,s.S_SHOOTER.hostility,s.S_SHOOTER.hit,s.S_SHOOTER.hr,
s.S_SHOOTER.arm.emg.emg0,s.S_SHOOTER.arm.emg.emg1,
s.S_SHOOTER.arm.roll,s.S_SHOOTER.arm.pitch,s.S_SHOOTER.arm.heading,s.S_SHOOTER.shot,s.S_SHOOTER.body.heading,s.S_SHOOTER.body.roll,s.S_SHOOTER.body.pitch,s.S_SHOOTER.head.heading,
s.S_SHOOTER.head.roll,s.S_SHOOTER.head.pitch
FROM Shooter_Table s

select * FROM Shooter_Table s
select * FROM Emg_Obj
select * FROM Arm_Obj
select * from table(Emg_Obj)


DECLARE
  DATA_SET SHOOTER := SHOOTER();
BEGIN
    SELECT SHOOTER( sysdate, numb, varc )  BULK COLLECT INTO  DATA_SET
    FROM SHOOTER_TABLE;

    INSERT INTO TBL_02( flag, numb, varc )
    SELECT * FROM Table( DATA_SET );
END;
/
CREATE TABLE Emg_Table
(s_index NUMBER NOT NULL, Emg Emg_Obj,
CONSTRAINT Emg_Table_PK PRIMARY KEY(s_index))

INSERT INTO Emg_Table
VALUES(
shooter_index_seq.nextval,
Emg (Emg_Obj(1,2,3,4,5,6,7,8))
)

