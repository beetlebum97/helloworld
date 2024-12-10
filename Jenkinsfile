pipeline {
    agent any
    environment {
        PYTHONPATH = "/home/davidvazquez/helloworld"
        FLASK_APP = "${env.PYTHONPATH}/app/api.py"
    }
    stages {
        stage('Get Code') {
            steps {
                echo "WORKSPACE: ${env.WORKSPACE}"
                sh '''
                uname -a
                cd $PYTHONPATH
                git pull origin master
                ls -la
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'No hace nada ^_^'
            }
        }
        stage('Tests') {
            parallel {
                stage('Unit') {
                    steps {
                        sh 'pytest --junitxml=result-unit.xml ${PYTHONPATH}/test/unit'
                    }
                }
                stage('Rest') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh 'flask run &'
                            sh '''
                                java -jar /home/davidvazquez/wiremock-standalone-3.10.0.jar --port 9090 --root-dir ${PYTHONPATH}/test/wiremock & 
                                while ! nc -z localhost 9090; do 
                                    sleep 3 
                                done
                            '''
                            sh 'pytest --junitxml=result-rest.xml ${PYTHONPATH}/test/rest/'
                        }
                    }
                }
            }
        }
        stage('Results') {
            steps {
                junit 'result*.xml'
            }
        }
    }
}
