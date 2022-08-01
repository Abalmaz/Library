def clearImage(){
    script.sh "docker stop $(docker ps -q) || docker rm $(docker ps -a -q) || docker rmi $(docker images -q | tail -n +2)"
}

def dockerLogin(){
    withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'PASS', usernameVariable: 'USER')])
    {
            sh "echo $PASS | docker login -u $USER --password-stdin"
    }
}

def dockerBuild(String imageName){
    script.sh "docker build -t $imageName ."
}

def dockerPush(String imageName){
    script.sh "docker push $imageName"
}

def buildImage(){
    clearImage()
    dockerLogin()
    dockerBuild(IMAGE_NAME)
    dockerPush(IMAGE_NAME)
}
return this