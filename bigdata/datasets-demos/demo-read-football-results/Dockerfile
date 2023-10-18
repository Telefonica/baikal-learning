FROM apache/spark:v3.3.2

USER root

# Create working directory

RUN mkdir /cwd
WORKDIR /cwd

# Install python

RUN apt update
RUN apt install python3.9 python3-pip -y

# Install dependencies

RUN python3 -m pip install pyspark==3.3.2 pandas

# Setup bash as entry point

ENTRYPOINT ["/bin/bash"]
