
# Switch to Neo4j official image for Java & GDS support
FROM neo4j:5.20

# Use root to install additional tools
USER root

WORKDIR /cse511

# Install Python, pip, and helper tools
RUN apt-get update && \
    apt-get install -y python3 python3-pip wget curl netcat unzip nano gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Java 21 (Eclipse Temurin)
RUN mkdir -p /etc/apt/keyrings && \
    wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /etc/apt/keyrings/adoptium.asc && \
    echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list && \
    apt-get update && \
    apt-get install -y temurin-21-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/temurin-21-jdk-arm64

# Upgrade pip and install Python dependencies
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install pandas pyarrow neo4j

# Download dataset and GDS plugin
RUN wget -O /var/lib/neo4j/import/yellow_tripdata_2022-03.parquet \
    https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet && \
    wget -O /var/lib/neo4j/plugins/neo4j-graph-data-science-2.21.0.jar \
    https://github.com/neo4j/graph-data-science/releases/download/2.21.0/neo4j-graph-data-science-2.21.0.jar

# Copy DataLoader script
COPY data_loader.py /cse511/data_loader.py

# Neo4j configuration & permissions
RUN mkdir -p /var/lib/neo4j/conf && \
    echo "server.default_listen_address=0.0.0.0" >> /var/lib/neo4j/conf/neo4j.conf && \
    echo "dbms.security.procedures.unrestricted=gds.*,apoc.*" >> /var/lib/neo4j/conf/neo4j.conf && \
    echo "dbms.security.procedures.allowlist=gds.*,apoc.*" >> /var/lib/neo4j/conf/neo4j.conf && \
    mkdir -p /var/lib/neo4j/import && \
    chmod 777 /var/lib/neo4j/import && \
    chown -R neo4j:neo4j /cse511 /var/lib/neo4j

# Switch back to neo4j user
USER neo4j

# Set initial password & load data at build time
RUN neo4j-admin dbms set-initial-password graphprocessing && \
    neo4j start && \
    sleep 15 && \
    python3 /cse511/data_loader.py && \
    neo4j stop

# Expose Neo4j ports
EXPOSE 7474 7687

# Keep container running
CMD ["neo4j", "console"]
