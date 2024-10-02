#!/bin/bash
set -e

# Create the pgvector extension
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE EXTENSION vector;"