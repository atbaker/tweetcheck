FROM python:2.7.8

# INSTALL NODE

# verify gpg and sha256: http://nodejs.org/dist/v0.10.31/SHASUMS256.txt.asc
# gpg: aka "Timothy J Fontaine (Work) <tj.fontaine@joyent.com>"
RUN gpg --keyserver pgp.mit.edu --recv-keys 7937DFD2AB06298B2293C3187D33FF9D0246406D

ENV NODE_VERSION 0.10.33
ENV NPM_VERSION 2.1.6

RUN curl -SLO "http://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz" \
    && curl -SLO "http://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
    && gpg --verify SHASUMS256.txt.asc \
    && grep " node-v$NODE_VERSION-linux-x64.tar.gz\$" SHASUMS256.txt.asc | sha256sum -c - \
    && tar -xzf "node-v$NODE_VERSION-linux-x64.tar.gz" -C /usr/local --strip-components=1 \
    && rm "node-v$NODE_VERSION-linux-x64.tar.gz" SHASUMS256.txt.asc \
    && npm install -g npm@"$NPM_VERSION" \
    && npm cache clear

# Configure local
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip install -r requirements/local.txt

RUN npm install -g bower
RUN bower install --allow-root

EXPOSE 8000

CMD [ "python", "tweetcheck/manage.py", "runserver", "0.0.0.0:8000"]
