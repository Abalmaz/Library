def gv

pipeline {
    agent any
    stages {
        stage("init"){
            steps{
                script{
                    gv = load "script.groovy"
                }
            }
        }
        stage("increment version"){
                    steps{
                        script{
                            echo "increment app version..."
                            echo "$GIT_COMMIT.take(6)-$BUILD_NUMBER"
                        }
                    }
                }
        stage("test") {
            steps {
                script {
                    echo "Run some test..."
                }
            }
        }
        stage("build image") {
            steps {
                script {
                    gv.buildImage()
                }
            }
        }
        stage("deploy") {
            steps {
                script {
                    echo "deploying..."
                }
            }
        }
    }
}
