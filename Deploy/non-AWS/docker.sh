#!/bin/bash
cd ../../News

docker build ./ -t news/sentiment:0.2
docker run --env-file=./.env.dev news/sentiment:0.2
