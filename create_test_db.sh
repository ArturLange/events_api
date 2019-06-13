#!/bin/bash

docker run -d --name test_db --rm -p 5433:5432 postgres:11 -c fsync=off
