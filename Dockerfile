
FROM ubuntu:14.04
MAINTAINER Fanf <fanf@fanf>

RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install python-pip python-dev python-twisted openssh-server telnetd 

RUN apt-get -y install git 

RUN mkdir /var/run/sshd
RUN echo '%wheel ALL=(ALL) ALL' >> /etc/sudoers
RUN sed -i '28s/.*/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN echo 'root:root' | chpasswd
RUN git clone https://github.com/fanff/wolfenscii.git

#RUN sed -i 's/root:x:0:0:root:\/root:\/bin\/bash/root:x:0:0:root:\/wolfenscii:wolfenscii_client.py/' /etc/passwd 
RUN chmod +x /wolfenscii/wolfenscii_client.py

EXPOSE 22
CMD /usr/sbin/sshd -D

