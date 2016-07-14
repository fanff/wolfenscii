
FROM ubuntu:14.04
MAINTAINER Fanf <fanf@fanf>

RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install python-pip python-dev python-twisted openssh-server telnetd 

RUN apt-get -y install git 

RUN mkdir /var/run/sshd

RUN git clone https://github.com/fanff/wolfenscii.git


RUN useradd wolf
RUN echo 'wolf:wolf' | chpasswd

RUN chmod +x /wolfenscii/wolfenscii_client.py

RUN sed -i 's/^wolf.*/wolf:x:1000:1000::\/wolfenscii:\/wolfenscii\/wolfenscii_client.py/' /etc/passwd 



EXPOSE 22
CMD /usr/sbin/sshd -D

