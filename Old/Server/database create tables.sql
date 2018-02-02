create table people(
	id int auto_increment,
	name varchar(30) not null,
	primary key (id)
);

create table locations(
	id int auto_increment,							-- null
	people_id int not null,							-- userObject.getId()
	time_stamp datetime not null,					-- now()
	locationXAxis float not null,					-- userObject.getLocationXAxis()
	locationYAxis float not null,					-- userObject.getLocationYAxis()
	locationZAxis float,							-- userObject.getLocationZAxis()
	width int,										-- null
	height int,										-- null
	primary key (id),
	foreign key (people_id) references people(id)
);

create table orientations(
	id int auto_increment,			-- null
	people_id int not null,			-- userObject.getId()
	time_stamp datetime not null,	-- now()
	headXAxis float,				-- userObject.getHeadXAxis()
	headYAxis float,				-- userObject.getHeadYAxis()
	headZAxis float,				-- userObject.getHeadZAxis()
	headHeading float,				-- userObject.getHeadHeading()
	headDegrees float,				-- userObject.getHeadDegrees()
	bodyXAxis float,				-- userObject.getBodyXAxis()
	bodyYAxis float,				-- userObject.getBodyYAxis()
	bodyZAxis float,				-- userObject.getBodyZAxis()
	bodyHeading float,				-- userObject.getBodyHeading()
	bodyDegrees float,				-- userObject.getBodyDegrees()
	primary key (id),
	foreign key (people_id) references people(id)
);

create table biometrics(
	id int auto_increment,			-- null
	people_id int not null,			-- userObject.getId()
	time_stamp datetime not null,	-- now()
	shot boolean not null,			-- userObject.getShot()
	roll int not null,				-- userObject.getRoll()
	pitch int not null,				-- userObject.getPitch()
	yaw int not null,				-- userObject.getYaw()
	emg_1 int not null,				-- emg[0]
	emg_2 int not null,				-- emg[1]
	emg_3 int not null,				-- emg[2]
	emg_4 int not null,				-- emg[3]
	emg_5 int not null,				-- emg[4]
	emg_6 int not null,				-- emg[5]
	emg_7 int not null,				-- emg[6]
	emg_8 int not null,				-- emg[7]
	primary key (id),
	foreign key (people_id) references people(id)
);

create table targabots(
	id int auto_increment,
	primary key (id)
);

create table targabotsLocations(
	id int auto_increment,
	time_stamp datetime not null,
	locationX float not null,
	locationY float not null,
	locationZ float not null,
	primary key (id)
);

create table targabotsStates(
	id int auto_increment,
	targabot_id int not null,
	location_id int not null,
	time_stamp datetime not null,
	slide int not null,
	degree int not null,
	hit boolean not null,
	hostile boolean not null,
	visible boolean not null,
	primary key (id),
	foreign key (targabot_id) references targabots(id),
	foreign key (location_id) references targabotLocations(id)
);

-- test database
create table test(
	id int auto_increment,				-- null
	people_id int not null,				-- userObject.getId()
	emg_1 int,								-- emg[0]
	emg_2 int,								-- emg[1]
	emg_3 int,								-- emg[2]
	emg_4 int,								-- emg[3]
	emg_5 int,								-- emg[4]
	emg_6 int,								-- emg[5]
	emg_7 int,								-- emg[6]
	emg_8 int,								-- emg[7]
	headXAxis float,					-- userObject.getHeadXAxis()
	headYAxis float,					-- userObject.getHeadYAxis()
	headZAxis float,					-- userObject.getHeadZAxis()
	bodyXAxis float,					-- userObject.getBodyXAxis()
	bodyYAxis float,					-- userObject.getBodyYAxis()
	bodyZAxis float,					-- userObject.getBodyZAxis()
	locationXAxis float,				-- userObject.getLocationXAxis()
	locationYAxis float,				-- userObject.getLocationYAxis()
	locationZAxis float,				-- userObject.getLocationZAxis()
	-- time_stamp datetime not null,	-- now()
	-- shot boolean not null,			-- userObject.getShot()
	-- roll int not null,				-- userObject.getRoll()
	-- pitch int not null,				-- userObject.getPitch()
	-- yaw int not null,				-- userObject.getYaw()
	primary key (id)
);
