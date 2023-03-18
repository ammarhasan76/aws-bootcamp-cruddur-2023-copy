# Week 1 — App Containerization

## MANDATORY TASKS
- [x] Containerize Application (Dockerfiles, Docker Compose)
- [x] Document the Notification Endpoint for the OpenAI Document
- [x] Write a Flask Backend Endpoint for Notifications
- [x] Write a React Page for Notifications
- [x] Run DynamoDB Local Container and ensure it works
- [x] Run Postgres Container and ensure it works

## Journal

21/FEB/2023  
Completed watching: How to Ask for Technical Help (Before You Ask For Help Watch This)  
https://www.youtube.com/watch?v=tDPqmwKMP7Y  
Study Notes:  
- Detail the error, incl screenshots
- Steps taken to reproduce the error
- Upload file(s) as a gist (gist.github.ciom...)
- gitpod + public repo = easy for someone else to launch your code and assist
- Use web browser inspector (console) to look at any errors
- Use print statements in code to help debug
- Use breakpoints to help debug

23/FEB/2023  
Completed watching: Grading Homework Summaries (Grading Homework Summaries)  
https://www.youtube.com/watch?v=FKAScachFgk&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=26  
Study Notes:
- Some specific highlights is nice
- No need to repeat items from the checklist
- Create Sections to help readability


23/FEB/2023  
Completed watching: Remember to Commit Your Code (Week 1- After Stream - Commit Your Code)  
https://www.youtube.com/watch?v=b-idMgFFcpg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=24  
Study Notes:  
- Don't forget to commit your changes!
- If you do forget and you are using GitPod - reopen the Workspace you were using and you should be able to commit the code


23/FEB/2023  
Watching: Week 1 - Live Streamed Video (Week 1 - App Containerization)  
https://www.youtube.com/watch?v=zJnNe5Nv4tE&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=23 (00h:00m to 00h:45m)  
Study Notes:
- Why Containerise the application
- Makes application portable
- Avoid envionrment configuration repition work
- Consistent environment between developers
- Consistent environment between dev -> uat -> prd
        
- Recommended	by @jamesspurin: linuxserver.io
- Docker Hub = Container Registry hosted by Docker co.
- OCI = Open Container Initiative, Docker Hub meets OCI standard

Action: confirmed I have dockerhub account  
Action: checked for extension, but Gitpod did not have the VSCode extension for Docker installed  
Action: installed VSCode Docker extension for local install and gitpod workspace  

- Docker image "scratch" = official base image  
- Dockers layers = union filesystem  
- What is a docker "volume"? = volume local to the running container

### Note
Got Codespaces up and running with config that matches GitPod Workspace
Interesting to note that when choosing to launch to local VSCode instance the extensions I defined get installed, I don't think I saw that with GitPod when launching VSCode locally (the terminal was still going to GitPod hosted container)

28/FEB/2023  
Worked on learning GitPod Workspace configuration

01/03/2023  
Worked on learning GitHub CodeSpaces configuration

#Note
I accidentally deleted my Workspace and when I started a new one I saw that I have lost my local install and extensions, so I went down the rabbit hole of gitpod.yml and devcontainer.json configuration, so that AWS CLI is always installed locally, and VSCode extensions do not need reinstalling.  
Ref: https://www.gitpod.io/docs/references/ides-and-editors/vscode-extensions

I found the same functionality difference, in that with CodeSpaces I can see and use "add extension to devcontainer" in browser or local VScode, whereas in gitpod I only see "add to gitpod.yml" in the browser.  
It has been a fun exercise learning how to configure gitpod and codespaces so that installations and extensions are preserved if I start from a new Github CodeSpace or GitPod Workspace.  
Additionally, by having out of sync local repos running in parallel in CodeSpaces and GitPod due to updating their config files, I learn the "git pull --rebase" command to fix my repo sync issues (successfully!)

Interesting references whilst researching:
https://code.visualstudio.com/docs/sourcecontrol/github
https://vscode.github.com/


## Containerise BackEnd

01/MAR/2023  
Watching: Week 1 - Live Streamed Video (Week 1 - App Containerization)  
https://www.youtube.com/watch?v=zJnNe5Nv4tE&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=23 (00h:45m to 01h:40m)  
Study Notes:  
```pip3 install -r requirements.txt```  
(this was executed in dev env)

==need to this in gitpod to stay in sync==

*Web server is running but 404'ing due to frontend_url and backend_url env var not being configured, the proper URL is /api/activities/home*

Action: (locally)  
`cd backend-flask
export FRONTEND_URL="*"
export BACKEND_URL="*"
python3 -m flask run --host=0.0.0.0 --port=4567`  
(make sure the port is unlocked/public, got to port take in vscode, open link and apped /api/activities/home to check all okay)

In Dockerfile:  
RUN = cmd creating a layer in the image  
CMD = cmd executed once the container is running

`unset FRONTEND_URL
unset BACKEND_URL
env | grep FRONTEND_URL
env | grep BACKEND_URL`  

Action: (locally - starting from home dir)  
`docker build -t backend-flask ./backend-flask`

*-t is tagging the container (name:tag so backend-flask:latest by default)  
./ from home/subdirectory*

Action: (run the container)  
`docker run --rm -p 4567:4567 -it backend-flask`

Problem due to missing ENV VARS

Action: (lets looks inside the container to see if ENV VARS are set) 
1. `docker exec -it ${CONTAINER_ID} /bin/bash`
2. attach shell using the Docker extension
(run the env command and you can see the two URL vars are not set)

Solution  
1. Add the ENV VARS in the Dockerfile  
2. Pass the ENV VARS to the docker  
if the ENV VARS are already set locally, you don't even need to explicitly pass the full VAR to the docker run command, so;
`docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask`
is the same as  
`docker run --rm -p 4567:4567 -it -e FRONTEND_URL -e BACKEND_URL backend-flask`  
single-quote the var value due to shell interpretation of what is in " "

02/MAR/2023  
Watching: Week 1 - Live Streamed Video (Week 1 - App Containerization)  
https://www.youtube.com/watch?v=zJnNe5Nv4tE&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=23 (01h:40m to 02h:00m)  
Study Notes:  

Action: (run container in background, ie returns the container ID and then gives back the command prompt)
`docker container run --rm -p 4567:4567 -d -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask`

Action: (alternative, also assign the containerid to an env var)  
`CONTAINER_ID=$(docker run --rm -p 4567:4567 -d -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask`  
`echo ${CONTAINER_ID}`  
`docker exec -it ${CONTAINER_ID} /bin/bash`

Action : (get Container Images or Running Container Ids)  
`docker ps` (see running containers)  
`docker ps -a` (need to use this to see stopped containers, if you run a container with -rm flag then when you stop a container the rm is automatic, for example for post-mortem troubleshooting, looking at container logs inside the container, but it's usual to sue -rm as containers are often run as disposable compute)  
`docker images` (to see all local images)

Action: (cURL to test the server from the terminal)  
`curl -X GET http://localhost:4567/api/activities/home -H "Accept: application/json" -H "Content-Type: application/json"`

## Containerise FrontEnd

Action: (to install NPM)  
`npm i`

Action:   
(create empty Dockerfile in frontend folder and copy contents from Andrew's journal)

Action: (could build the container like the backend)
`cd ..` (switch to home folder)  
`docker build -t frontend-react-js ./frontend-react-js`  
`docker run -p 3000:3000 -d frontend-react-js`

Build Multiple Containers using docker compose  
Action:  
(Create empty docker-compose.yml file at the root of your project and copy contents from Andrew's journal)

Action:
`docker compose up`  
or  
right-click on the file in VSCode and click 'Compose Up'

Note: All working, yay!!! :joy:

Action: Mount directories so we can make changes while we code (change message in home_acitivities.py)  
Note: notice change instantly reflected as the container has mounted the local directory as per docker compose yaml file.

Action: (stop both containers in one go) 
`docker stop containerid1 containerid2`  
eg docker stop d7b8086ef2e1 2dfe51f7dbe7

02/MAR/2023  
Watched: Chirag's Week 1 - Spending Considerations (Gitpod, Github Codespaces, AWS Cloud9 and Cloudtrail)  
https://www.youtube.com/watch?v=OAMHu1NiYoI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=24  
Study Notes:

GitPod  
50hrs usage / month (actually 500 credits a month)  
Std: 4 cores, 8gb ram, 30gb storage  
Avoid running Workspaces in parallel as it will expend credits  
30mins timeout helps avoid using credits when you forget to stop a Workspace  
Calculator: https://www.gitpod.io/pricing

Github CodeSpaces  
60hrs/month @ 2core, 4gb ram, 15gb storage  
30hrs/month @ 4core, 8gb ram, 15gb storage  
https://github.com/features/codespaces  
https://github.com/pricing/calculator  

AWS Cloud9  
Free t2.micro instance in your account  
Avoid as it uses your ec2 t2 credits  
https://aws.amazon.com/cloud9/pricing/  
Note: its still cheap: If you use the default settings running an IDE for 4 hours per day for 20 days in a month with a 30-minute auto-hibernation setting your monthly charges for 90 hours of usage would be:  
Compute fees*	$1.05	t2.micro Linux instance at $0.0116/hour x 90 total hours used per month = $1.05  
Storage fees	$1.00	$0.10 per GB-month of provisioned storage x 10-GB storage volume = $1.00  
Total monthly fees	$2.05

CloudTrail  
Avoid unless necessary usage of services (for dev env)  
If need to use, minimize usage of options:  
Deselect KMS  
Deselect Data Events  
Deselect Inisghs Events  
Note: default is 90 days of CT data so you can still have some data even if not swticheed on

02/MAR/2023  
Watched: Week 1 - Create the notification feature (Backend and Front)  
https://www.youtube.com/watch?v=k-_o0cCpksk&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=27  
Study Notes: 

https://www.openapis.org/  
https://readme.com/

- document a new api endpoint in OpenAPI

Action: click show preview with default browser icon (top-right) to see openai (swagger view of the APIs)  
Action: can check OpenAPI specification at: https://spec.openapis.org/oas/latest.html  
Action: click on split tab to help with coding a new endpoint based on existing endpoint  
$ref: '#/components/schemas/Activity' = look at the bottom of the file, the schema is defined there and using the OpenAPI preview, you can see the schema for the new endpoint is updated with the schema details

https://www.toptal.com/ruby-on-rails/rails-service-objects-tutorial#:~:text=What%20is%20a%20service%20object,API%20like%20posting%20a%20tweet.

- implement a Backend endpoint (Notifications) - please check repo

- implement a Frontend UI  -- please check repo

02/MAR/2023  
Watched: Week 1 - Run DynamoDB Local Container and ensure it works and Run Postgres Container and ensure it works (Week 1 - DynamoDB and Postgres vs Docker)  
https://www.youtube.com/watch?v=CbQNMaa6zTg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=28  
Study Notes:

Action: update docker-compose.yml to add DynamoDB Local and Postgres

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html

Example of using DynamoDB Local:
https://github.com/100DaysOfCloud/challenge-dynamodb-local

Action: (need to get aws defaults entered)
aws configure
access key: (get from AWS console)
secret access key: (get from AWS console)

Action: updated gitpod.yml for aws, postgres installations and added postgres extension

Action: using extension add database connection

Action: connect through the terminal
psql -h localhost -U postgres
\d
\t
\dl
\l

03/MAR/2023  
Watched Ashish's Week 1 - Container Security Considerations (Top 10 Docker Container Security Best Practices with Tutorial)  
https://www.youtube.com/watch?v=OjZz4D0B-cA&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=25  
StudyNotes:
- Docker Security Components:  
- Docker & Host Configuration
- Securiing Images 
- Secret Management
- Application Security
- Data Security
- Monitoring Containers
- Compliance Framework

10 Container Security Best Practices:
- Keep Host & Docker Updated to latest security Patches
- Docker daemon & containers should run in non-root user mode

- Image Vulnerability Scanning
- Trusting a Private vs Public Image Registry

- No Sensitive Data in Docker files or Images
- Use Secret Management Services to Share secrets

- Read only File system and Volume for Docker
- Separate databases for long term storage

- Use DevSecOps practices while building application security
- Ensure all Code is tested for vulnerabilities before production use

Tools & Demos:

Snyk: repo & image scanning
- Can run in terminal (synk container test CONTAINERIMAGENAME)

Secret Management Tools 
- AWS Secret Manager or Hashicorp Vault

AWS Secret Manager:  
- Charged per secret and for API calls  
- Use automatic rotation

Image Vulnerability Scanning
- AWS Inpector or CLAIR

AWS Inspector (EC2 images, Container images, Container registries)
- Scanning
-Can feed info into/results related AWS services

AWS Managed Container Services
- AWS ECS, AWS EKS, AWS Fargate, AWS App Runner, AWS CoPilot

Integration with AWS Service
- Uses automation to provision containers at scale with speed & security

Further Learning Topics:
- Docker Host & Container Security
- Docker Image Registry
- Docker Security Benchmarks
- Docker Network Security
- Docker container secrets
- Docker Read-Only filesystem & volumes

Appendix:
- Cloud Security BootCamp Tools ►  https://cloudsecuritybootcamp.com
- Follow me on Twitter  ►  https://twitter.com/hashishrajan

Tools Used in this Video:
- AWS Inspector: https://aws.amazon.com/inspector/
- AWS Secret Manager: https://aws.amazon.com/secrets-manager/
- Clair: https://github.com/quay/clair
- Snyk Container/ Snyk Open Source Tool: https://snyk.co/cloudbootcamp
- Snyk Cli - https://docs.snyk.io/snyk-cli/install-the-snyk-cli

Github Repositories:
- Vulnerable Dockerfile - https://github.com/snyk-labs/docker-goof
- Docker Compose Documentation - https://docs.docker.com/compose/gettingstarted/

## Challenge Tasks

03/MAR/2023
Push and tag a image to DockerHub
![image](https://user-images.githubusercontent.com/22940535/222759396-a33f8700-2c92-407b-9593-f1b31b0c8bcf.png)

Ran out of time, will need to catch up on extension/challenge tasks, even if it is after grading

03/MAR/2023  
Edited Markdown to make readability and formatting much nicer to look at :joy:
