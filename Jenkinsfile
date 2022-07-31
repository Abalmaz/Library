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
                            GIT_HUSH=GIT_COMMIT.substring(0, 8)
                            echo "increment app version..."
                            env.IMAGE_NAME=GIT_HUSH-BUILD_NUMBER
                            echo "$IMAGE_NAME"
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
