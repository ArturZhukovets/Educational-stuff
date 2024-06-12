# Server basic configuration
# Configure server with openssh-server and with already initialized ssh key in
# authorized keys folder.
FROM ubuntu:latest

# Update the package list and install any desired packages
RUN apt-get update && apt-get install -y \
    nano \
    curl \
    wget \
    vim \
    openssh-server

# Create the SSH directory
RUN mkdir /var/run/sshd

# Set root password (you can change it to your desired password)
RUN echo 'root:password' | chpasswd

RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    touch /root/.ssh/authorized_keys && \
    chmod 600 /root/.ssh/authorized_keys

# copy my ssh key to ubuntu server
COPY key.pub /root/.ssh/authorized_keys

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
