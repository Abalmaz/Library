def buildImage(){
    echo "building..."
    withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'PASS', usernameVariable: 'USER')])
    {
        sh 'docker --version'
    }
}
return this