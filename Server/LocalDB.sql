CREATE TYPE Loc_Obj AS OBJECT
(x NUMBER, y NUMBER, z NUMBER)

CREATE TYPE Orient_Obj AS OBJECT
(heading FLOAT, roll FLOAT, pitch FLOAT)

DROP TYPE Emg_Obj;
CREATE TYPE Emg_Obj AS VARRAY(10) OF NUMBER;

DROP TYPE Arm_Obj;
CREATE TYPE Arm_Obj AS OBJECT
(emg Emg_Obj, roll FLOAT, pitch FLOAT, heading FLOAT);

DROP TYPE ENTITY;
CREATE TYPE ENTITY AS OBJECT
(id NUMBER, loc Loc_Obj, hostility NUMBER, hit NUMBER) NOT FINAL;

DROP TYPE SHOOTER;
CREATE TYPE SHOOTER UNDER ENTITY
(hr NUMBER, arm Arm_Obj, shot NUMBER, body Orient_Obj, head Orient_Obj) NOT FINAL;

DROP TYPE TARGET;
CREATE TYPE TARGET UNDER ENTITY
(visible NUMBER)

DROP TABLE Target_Table;
CREATE TABLE Target_Table
(t_index NUMBER NOT NULL, t_date TIMESTAMP, t_target Target,
CONSTRAINT target_PK PRIMARY KEY(t_index));

CREATE SEQUENCE target_index_seq
  START WITH 1
  INCREMENT BY 1;
  
DROP TABLE Shooter_Table;
CREATE TABLE Shooter_Table
(s_index NUMBER NOT NULL, s_date TIMESTAMP, s_shooter SHOOTER,
CONSTRAINT shooter_PK PRIMARY KEY(s_index));

CREATE SEQUENCE shooter_index_seq
  START WITH 1
  INCREMENT BY 1;


INSERT INTO Target_Table 
VALUES(
target_index_seq.nextval,
CURRENT_TIMESTAMP,
Target(1,Loc_Obj(2,3,4),5,6,7));

SELECT *
FROM Target_Table t;

INSERT INTO Shooter_Table
VALUES(
shooter_index_seq.nextval,
CURRENT_TIMESTAMP,
SHOOTER(
1,
Loc_Obj(21,61,78),
1,
0,
61,
Arm_Obj(Emg_Obj(1,2,3,4,5,6,7,8),23.2,31.5,87.3),
0,
Orient_Obj(32.4,57.3,27.2),
Orient_Obj(21.4,77.3,29.2)));

Select s.S_INDEX,s.S_DATE,s.S_SHOOTER.Id,s.S_SHOOTER.Loc.x,s.S_SHOOTER.Loc.y,s.S_SHOOTER.Loc.z,s.S_SHOOTER.hostility,s.S_SHOOTER.hit,s.S_SHOOTER.hr,s.S_SHOOTER.arm.emg,
s.S_SHOOTER.arm.roll,s.S_SHOOTER.arm.pitch,s.S_SHOOTER.arm.heading,s.S_SHOOTER.shot,s.S_SHOOTER.body.heading,s.S_SHOOTER.body.roll,s.S_SHOOTER.body.pitch,s.S_SHOOTER.head.heading,
s.S_SHOOTER.head.roll,s.S_SHOOTER.head.pitch
FROM Shooter_Table s;
