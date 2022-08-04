def gv

pipeline {
    agent any
    environment {
        HASH_COMMIT = GIT_COMMIT.substring(0, 8)
        IMAGE_NAME="abalmaz/library:$HASH_COMMIT-$BUILD_NUMBER"
    }
    stages {
        stage("init"){
            steps{
                script{
                    gv = load "script.groovy"
                }
            }
        }
        stage("Build image") {
            steps {
                script {
                    gv.buildImage()
                }
            }
        }
        stage("Run tests") {
            steps {
                script {
                    gv.runTest()
                }
            }
            post {
                    always {
                         step([$class: 'CoberturaPublisher',
                          coberturaReportFile: 'reports/coverage.xml',
                         ])
                    }
                }
        }
        stage("Push image") {
                    steps {
                        script {
                            gv.pushImage()
                        }
                    }
                }
        stage("provision server"){
            environment {
                AWS_ACCESS_KEY_ID = credentials('jenkins_aws_access_key_id')
                AWS_SECRET_ACCESS_KEY = credentials('jenkins_aws_secret_access_key')
                TF_VAR_jenkins_ip = "34.170.207.108/32"
            }
            steps {
                script {
                    gv.provisionServer()
                }
            }
        }
        stage("deploy") {
            environment {
                DOCKER_CREDS = credentials('docker-hub')
            }
            steps {
                script {
                    gv.deployOnEC2()
                }
            }
        }
    }
}
