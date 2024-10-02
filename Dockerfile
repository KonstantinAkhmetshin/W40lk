# Use the official PostgreSQL image
FROM postgres:latest

# Set environment variables
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=user
ENV POSTGRES_DB=postgres

# Install pgvector extension
RUN apt-get update && \
    apt-get install -y postgresql-server-dev-all && \
    apt-get install -y git build-essential && \  
    git clone --branch master https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && make install && \
    cd .. && rm -rf pgvector && \
    apt-get remove --purge -y git postgresql-server-dev-all build-essential && \ 
    apt-get autoremove -y && \
    apt-get clean

# Copy initialization script to create the extension
COPY init-db.sh /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port
EXPOSE 5432