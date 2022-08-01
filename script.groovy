def buildImage(){
    echo "building..."
    withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'PASS', usernameVariable: 'USER')])
    {
        sh "docker stop $(docker ps -q) || docker rm $(docker ps -a -q) || docker rmi $(docker images -q | tail -n +2)"
        echo "Build the Docker image..."
        sh "docker build -t $IMAGE_NAME ."
        sh "echo $PASS | docker login -u $USER --password-stdin"
        sh "docker push $IMAGE_NAME"
    }
}
return this