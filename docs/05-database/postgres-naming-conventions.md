# PostgreSQL Naming Conventions

## Tablas

snake_case plural

Ejemplos:

users
projects
project_phases

## PK

pk_<table>

## FK

fk_<table>_<referenced_table>

## Índices

idx_<table>_<column>

## Unique

uq_<table>_<column>

## Migraciones

YYYYMMDDHHMM_description
