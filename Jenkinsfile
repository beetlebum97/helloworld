pipeline {
    agent { label 'maestro'  // Nodo ejecutor
    }
    environment {
        URL_REPO = 'https://github.com/beetlebum97/helloworld.git'
        PYTHONPATH = "${env.WORKSPACE}"
        FLASK_APP = "${env.WORKSPACE}/app/api.py"
    }
    stages {
        stage('Get Code') {
            steps {
                script {
                    // Comprobar si el repositorio ya existe
                    if (fileExists('.git')) {
                        echo 'Repositorio ya existe, actualizando...'
                        sh 'git pull origin master'
                    } else {
                        echo 'Clonando el repositorio...'
                        sh 'git clone ${URL_REPO} .'
                    }
                }
                sh 'uname -a'
                sh 'whoami ; hostname ; hostname -I'
                echo "WORKSPACE: ${env.WORKSPACE}"
                sh 'ls -la'
            }
        }
        stage('Build') {
            steps {
                echo 'La etapa no hace nada (^_^)'
            }
        }
        stage('Tests') {
            parallel {
                stage('Unit') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {    // Continua aunque falle algún test
                            sh 'pytest --junitxml=result-unit.xml ${PYTHONPATH}/test/unit'
                        }    
                    }
                }
                stage('Rest') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {    // Continua aunque falle algún test
                            sh 'flask run &'
                            // Confirmar arranque Wiremock antes de los test
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
        }
        stage('Results') {
            steps {
                junit 'result*.xml'
            }
        }
    }
    post {
        always {
            cleanWs()  // Limpiar workspace
        }
    }
}
