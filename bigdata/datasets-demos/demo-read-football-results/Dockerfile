FROM apache/spark:3.3.3-scala2.12-java11-python3-ubuntu

# Set user root to perform admin actions

USER root

# Configuration

ENV JAR_DEPENDENCIES org.apache.spark:spark-avro_2.12:3.3.3,com.telefonica.baikal:spark-sdk_2.12:2.2.0
ENV REMOTE_REPOSITORIES https://4p-public-artifacts.s3.amazonaws.com/baikal/releases/,https://repo.osgeo.org/repository/release/

# Prepare path

ENV PATH /opt/spark/bin:$PATH

# Create download folders

ENV JARS_DIR /dependecies/jars
ENV POMS_DIR /dependecies/poms

RUN mkdir -p $JARS_DIR
RUN mkdir -p $POMS_DIR

# Create working directory

RUN mkdir /cwd
WORKDIR /cwd

# Update apt

RUN apt update
RUN apt install -y maven

# Download dependencies
# Plugin doc: https://maven.apache.org/plugins-archives/maven-dependency-plugin-2.8/get-mojo.html
# Plugin doc: https://maven.apache.org/plugins-archives/maven-dependency-plugin-2.8/copy-dependencies-mojo.html

RUN set -e && for artifact in $(echo $JAR_DEPENDENCIES | tr "," "\n"); do \
  mvn -T 4 -e dependency:get \
  -DremoteRepositories="$REMOTE_REPOSITORIES" \
  -Dartifact="$artifact" \
  -Ddest=$JARS_DIR \
  -Dmaven.wagon.http.retryHandler.count=6 \
  -Dmaven.wagon.httpconnectionManager.ttlSeconds=25 \
  ; done

RUN set -e && for artifact in $(echo $JAR_DEPENDENCIES | tr "," "\n"); do \
  mvn -T 4 -e dependency:get \
  -DremoteRepositories="$REMOTE_REPOSITORIES" \
  -Dartifact="$artifact:pom" \
  -Ddest=$POMS_DIR \
  -Dmaven.wagon.http.retryHandler.count=6 \
  -Dmaven.wagon.httpconnectionManager.ttlSeconds=25 \
  ; done

RUN set -e && if [ ! -z "$(ls -A $POMS_DIR)" ]; then for pomfile in $POMS_DIR/*.pom; do \
  mvn -T 4 -e dependency:copy-dependencies \
  -f $pomfile -DoutputDirectory=$JARS_DIR \
  -DincludeScope=runtime \
  -Dmaven.wagon.http.retryHandler.count=3 \
  -Dmaven.wagon.httpconnectionManager.ttlSeconds=25 \
  ; done \
  ; fi

RUN cp /dependecies/jars/* /opt/spark/jars/

USER spark

ENTRYPOINT ["/bin/bash"]