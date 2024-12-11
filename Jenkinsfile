pipeline {
    agent any
    environment {
        PYTHONPATH = "${env.WORKSPACE}/helloworld"
        FLASK_APP = "${env.PYTHONPATH}/app/api.py"
    }
    stages {
        stage('Get Code') {
            steps {
                sh 'uname -a'
		echo "WORKSPACE: ${env.WORKSPACE}"
		echo 'Jenkinsfile descarga código fuente'
            }
        }
        stage('Build') {
            steps {
                echo 'No hace nada (^_^)'
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
                        sh 'flask run &'
                        sh '''
                            java -jar /opt/unir/wiremock-standalone-3.10.0.jar --port 9090 --root-dir ${PYTHONPATH}/test/wiremock & 
                            while ! nc -z localhost 9090; do 
                                sleep 2 
                            done
                            '''
                        sh 'pytest --junitxml=result-rest.xml ${PYTHONPATH}/test/rest/'
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
