def buildImage(){
    echo "building..."
    sh 'docker image prune -a --force --filter "label=maintainer=abalmaz"'
    echo "Build the Docker image..."
    sh "docker build -t $IMAGE_NAME ."
}

def pushImage(){
    echo "Pushing..."
    withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'PASS', usernameVariable: 'USER')])
    {
        sh "echo $PASS | docker login -u $USER --password-stdin"
        sh "docker push $IMAGE_NAME"
    }
}

def runTest(){
    sh "docker start db || docker run -d -e POSTGRES_HOST_AUTH_METHOD=trust --rm --name='db' postgres:9.6"
    sh "docker run -v $WORKSPACE/reports:/app/reports  --rm --link=db:db $IMAGE_NAME python manage.py jenkins --enable-coverage"
}

def provisionServer(){
    dir('terraform') {
        sh "terraform init"
        TR_APPLY_STATUS = sh(
             script: "terraform plan -detailed-exitcode",
             returnStatus: true
        )
        sh "terraform apply --auto-approve"
        EC2_PUBLIC_IP = sh(
            script: "terraform output ec2_public_ip",
            returnStdout: true
        ).trim()
    }
}

def deployOnEC2(){

    echo "deploying docker image to EC2..."

    if(TR_APPLY_STATUS == 2){
        echo "waiting for EC2 server to initialize"
        sleep(time: 90, unit: "SECONDS")
    }

    def shellCmd = "bash ./server-cmds.sh ${IMAGE_NAME} ${DOCKER_CREDS_USR} ${DOCKER_CREDS_PSW}"
    def ec2Instance = "ec2-user@${EC2_PUBLIC_IP}"

    sshagent(['library-server-ssh']) {
        sh "scp -o StrictHostKeyChecking=no server-cmds.sh ${ec2Instance}:/home/ec2-user"
        sh "scp -o StrictHostKeyChecking=no docker-compose.yml ${ec2Instance}:/home/ec2-user"
        sh "scp -o StrictHostKeyChecking=no nginx.conf ${ec2Instance}:/home/ec2-user"
        sh "ssh -o StrictHostKeyChecking=no ${ec2Instance} ${shellCmd}"
    }
}

return this