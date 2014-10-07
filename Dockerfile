FROM fedora:latest
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
RUN yum install -y wget
RUN yum install -y gcc
RUN yum install -y redis
RUN yum install -y git libgit2 libgit2-devel
RUN yum install -y python3 python3-devel python3-pip
RUN yum install -y libev libev-devel
RUN yum install -y supervisor
RUN wget http://download.rethinkdb.com/centos/6/`uname -m`/rethinkdb.repo -O /etc/yum.repos.d/rethinkdb.repo
RUN yum install -y rethinkdb
RUN yum install -y libffi libffi-devel
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN python3-pip install git+https://github.com/ryansb/gitsniffer.git@feature/celery
RUN mkdir /var/log/celery
EXPOSE 22 8080
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
