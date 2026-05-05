# Project Overview

This project is about building a tool called swiftdeploy that automatically builds and manages application stacks using predefined configuration.

Instead of manually writing deployment files, this project demonstrates a more advanced pattern known as Infrastructure as Code (IaC). Here, the manifest.yaml acts as the single source of truth, and the tool generates nginx.conf and docker-compose.yml from it. This ensures consistency, reduces manual errors, and makes deployments repeatable.

## What You Need Before Running

- Docker and Docker compose
- Python3
- pyaml and jinja2 python packages
- nginx

## How to Get Started

- Clone this repo
- Build the Docker image
- Run ./swiftdeploy validate

## How to Use Each Command

### init
Parse manifest → generate nginx.conf + docker-compose.yml from templates
`./swiftdeploy init`

### validate
5  pre-flight checks, exit non-zero on any failure, and print a clear pass/fail for the checks
`./swiftdeploy validate`

### deploy
Runs init, brings up the stack, and blocks until health checks pass or 60s timeout
`./swiftdeploy deploy`

### promote
Switches deployment mode with a rolling service restart
`./swiftdeploy promote stable` or  `./swiftdeploy promote canary`

### teardown
Removes all containers, networks, and volumes. --clean deletes generated configs
`./swiftdeploy teardown` or `./swiftdeploy teardown --clean`


## Folder Layout

swiftdeploy-project/
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── templates/
│   ├── docker-compose.yml.j2
│   └── nginx.conf.j2
├── manifest.yaml
├── README.md
└── swiftdeploy