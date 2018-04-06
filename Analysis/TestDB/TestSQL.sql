select * from TARGET_TABLE

-- Fromo Kyle's 1nd query in GUI
(SELECT
    s.S_INDEX,         -- 0
    s.S_DATE AS time,  -- 1
    s.S_SHOOTER.Id AS id, -- 2
    s.S_SHOOTER.Loc.x AS x, -- 3
    s.S_SHOOTER.Loc.y AS y, -- 4
    s.S_SHOOTER.shot AS shot, -- 5
    NULL AS hit, -- 6
    NULL AS visible, -- 7
    s.S_SHOOTER.head.heading AS heading, -- 8
    s.S_SHOOTER.arm.emg.emg0 AS emg0, -- 9
    s.S_SHOOTER.arm.emg.emg1 AS emg1, -- 10
    s.S_SHOOTER.arm.emg.emg2 AS emg2, -- 11
    s.S_SHOOTER.arm.emg.emg3 AS emg3, -- 12
    s.S_SHOOTER.arm.emg.emg4 AS emg4, -- 13
    s.S_SHOOTER.arm.emg.emg5 AS emg5, -- 14
    s.S_SHOOTER.arm.emg.emg6 AS emg6, -- 15
    s.S_SHOOTER.arm.emg.emg7 AS emg7, -- 16
    s.S_SHOOTER.arm.roll AS ARM_ROLL, -- 17
    s.S_SHOOTER.arm.pitch AS ARM_PITCH, -- 18
    s.S_SHOOTER.arm.heading AS ARM_YAW -- 19
    FROM Shooter_Table s WHERE s.S_INDEX>15525)
    UNION ALL
    (SELECT t.T_INDEX, -- 0
    t.T_DATE AS time, -- 1
    t.T_TARGET.ID AS id, -- 2
    t.T_TARGET.Loc.x AS x, -- 3
     t.T_TARGET.Loc.y AS y, -- 4
     NULL AS shot, -- 5
      t.T_TARGET.hit AS hit, -- 6
       t.T_TARGET.visible AS visible, -- 7
        NULL AS heading, -- 8
         NULL AS emg0, -- 9
         NULL AS emg1, -- 10
         NULL AS emg2, -- 11
         NULL AS emg3, -- 12
         NULL AS emg4, -- 13
         NULL AS emg5, -- 14
         NULL AS emg6, -- 15
         NULL AS emg7, -- 16
          NULL AS ARM_ROLL, -- 17
           NULL AS ARM_PITCH, -- 18
           NULL AS ARM_YAW -- 19
   FROM Target_Table t
   WHERE  t.T_INDEX>1080)
   ORDER BY time


-- Fromo Kyle's 2nd query in GUI
    SELECT
    max(s.S_SHOOTER.Loc.x), max(t.T_TARGET.Loc.x), min(s.S_SHOOTER.Loc.x), min(t.T_TARGET.Loc.x), max(
        s.S_SHOOTER.Loc.y), max(t.T_TARGET.Loc.y), min(s.S_SHOOTER.Loc.y), min(t.T_TARGET.Loc.y)
    FROM
    Shooter_Table
    s, Target_Table t
    WHERE
    t.T_INDEX > 1080
    AND
    s.S_INDEX < 15525
