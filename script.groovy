def buildImage(){
    echo "building..."
    withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'PASS', usernameVariable: 'USER')])
    {
        echo "Build the Docker image..."
        sh "docker build -t abalmaz:library:$IMAGE_NAME ."
        sh "echo $PASS | docker login -u $USER --password-stdin"
        sh "docker push abalmaz:library:$IMAGE_NAME"
    }
}
return this