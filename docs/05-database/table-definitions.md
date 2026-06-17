# Table Definitions (Deep Dive)

## organizations

id UUID PK
name VARCHAR(200) NOT NULL
status VARCHAR(30) NOT NULL
created_at TIMESTAMP NOT NULL

## users

id UUID PK
organization_id UUID NOT NULL
team_id UUID NULL
manager_id UUID NULL
email VARCHAR(320) NOT NULL
full_name VARCHAR(200) NOT NULL
role VARCHAR(30) NOT NULL
status VARCHAR(30) NOT NULL

## projects

id UUID PK
organization_id UUID NOT NULL
name VARCHAR(200) NOT NULL
description TEXT NULL
status VARCHAR(30) NOT NULL

## project_phases

id UUID PK
project_id UUID NOT NULL
name VARCHAR(200) NOT NULL
status VARCHAR(30) NOT NULL

## priorities

id UUID PK
phase_id UUID NOT NULL
owner_id UUID NOT NULL
week_period DATE NOT NULL
title VARCHAR(300) NOT NULL
description TEXT NULL
status VARCHAR(30) NOT NULL

## tasks

id UUID PK
priority_id UUID NOT NULL
title VARCHAR(300) NOT NULL
status VARCHAR(30) NOT NULL
