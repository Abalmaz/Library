def gv

pipeline {
    agent any
    environment {
        HUSH_COMMIT = GIT_COMMIT.substring(0, 8)
        IMAGE_NAME="abalmaz/library:$HUSH_COMMIT-$BUILD_NUMBER"
    }
    stages {
        stage("init"){
            steps{
                script{
                    gv = load "script.groovy"
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
        stage("test") {
            steps {
                script {
                    echo "Run some test..."
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
                    dir('terraform') {
                        sh "terraform init"
                        sh "terraform apply --auto-approve"
                        EC2_PUBLIC_IP = sh(
                            script: "terraform output ec2_public_ip",
                            returnStdout: true
                        ).trim()
                    }
                }
            }
        }
        stage("deploy") {
            steps {
                script {
                    echo "Waiting for EC2 server checking..."
                    sleep(time: 90, unit: "SECONDS")

                    echo "deploying docker image to EC2..."

                    def shellCmd = "bash ./server-cmds.sh ${IMAGE_NAME}"
                    def ec2Instance = "ec2-user@${EC2_PUBLIC_IP}"

                    sshagent(['library-server-ssh']) {
                        sh "scp -o StrictHostKeyChecking=no server-cmds.sh ${ec2Instance}:/home/ec2-user"
                        sh "scp -o StrictHostKeyChecking=no docker-compose.yml ${ec2Instance}:/home/ec2-user"
                        sh "ssh -o StrictHostKeyChecking=no ${ec2Instance} ${shellCmd}"
                    }
                }
            }
        }
    }
}
