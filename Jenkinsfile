pipeline {
    agent { label 'maestro'     // Nodo ejecutor
    }
    environment {
        PYTHONPATH = "${env.WORKSPACE}"
        FLASK_APP = "${env.WORKSPACE}/app/api.py"
    }
    stages {
        stage('Get Code') {
            steps {
                sh 'whoami ; hostname ; hostname -I; uname -a'      // Info Sistema
                git branch: 'master', url:'https://github.com/beetlebum97/helloworld.git'   // Clonar repo y posicionarse en rama master
                echo "WORKSPACE: ${env.WORKSPACE}"
                sh 'git rev-parse --abbrev-ref HEAD'    // Rama actual
		sh 'ls -la'
            }
        }
        stage('Build') {
            steps {
                echo 'No hace nada (^_^)'
            }
        }
        stage('Tests') {
            parallel {                  // Ejecución en paralelo
                stage('Unit') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {           // Continuar aunque falle la etapa
                            sh 'pytest --junitxml=result-unit.xml ${PYTHONPATH}/test/unit'
                        }    
                    }
                }
                stage('Rest') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {   
                            sh '''
                                n=0
                                flask run &
                                while ! nc -z localhost 5000; do
                                    sleep 1
                                    n=$((n+1))
                                done
                                echo "Flask arrancó en $n segundos"
                            '''
                            sh '''
                                n=0
                                java -jar /opt/unir/wiremock-standalone-3.10.0.jar --port 9090 --root-dir ${PYTHONPATH}/test/wiremock & 
                                while ! nc -z localhost 9090; do
                                    sleep 1
                                    n=$((n+1))
                                done
                                echo "Wiremock arrancó en $n segundos"
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
        always {            // Realizar siempre la tarea (stage ok/ko)
            cleanWs()       // Eliminar archivos del workspace
        }
    }
}
