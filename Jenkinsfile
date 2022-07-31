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
                            HASH_COMMIT=${GIT_COMMIT:0:5}
                            echo "$HASH_COMMIT-$BUILD_NUMBER"
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
