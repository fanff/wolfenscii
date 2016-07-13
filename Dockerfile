
FROM ubuntu:14.04
MAINTAINER Fanf <fanf@fanf>

RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install python-pip python-dev python-twisted openssh-server telnetd 

RUN apt-get -y install git 

RUN mkdir /var/run/sshd
RUN echo '%wheel ALL=(ALL) ALL' >> /etc/sudoers

# DELETE
RUN sed -i '28s/.*/PermitRootLogin yes/' /etc/ssh/sshd_config

# DELETE
RUN echo 'root:root' | chpasswd
RUN git clone https://github.com/fanff/wolfenscii.git

# DELETE
RUN sed -i '28s/.*/PermitRootLogin no/' /etc/ssh/sshd_config

RUN useradd wolf
RUN echo 'wolf:wolf' | chpasswd

# DELETE
RUN chmod +x /wolfenscii/wolfenscii_client.py

RUN sed -i 's/^wolf.*/wolf:x:1000:1000::\/wolfenscii:\/wolfenscii\/wolfenscii_client.py/' /etc/passwd 

#wolf:x:1000:1000::/wolfenscii:/wolfenscii/wolfenscii_client.py


EXPOSE 22
CMD /usr/sbin/sshd -D
