pipeline {
    agent { label 'maestro'    
    }
    environment {
        PYTHONPATH = "${env.WORKSPACE}"
        FLASK_APP = "${env.WORKSPACE}/app/api.py"
    }
    // DESCARGA CÓDIGO FUENTE
    stages {
        stage('Get Code') {
            steps {
                sh 'whoami ; hostname ; hostname -I; uname -a'      
                git branch: 'master', url:'https://github.com/beetlebum97/helloworld.git'   
                echo "WORKSPACE: ${env.WORKSPACE}"
                sh 'git rev-parse --abbrev-ref HEAD'
		sh 'ls -la'
            }
        }
        // PRUEBAS UNITARIAS 
        stage('Unit') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {           
                
                    // Ejecutar las pruebas unitarias y generar resultados y datos de cobertura.
                    sh 'pytest --junitxml=result-unit.xml --cov=app --cov-branch --cov-report=xml:coverage.xml --cov-config=/opt/unir/.coveragerc --cov-report=term-missing test/unit'
                    
                    // Publicar los resultados de las pruebas unitarias.
                    junit 'result-unit.xml'
                    
                    // Guardar datos de cobertura.
                    stash name: 'test-coverage', includes: 'coverage.xml'
                }    
            }
        }
        // PRUEBAS DE INTEGRACIÓN
        stage('Rest') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {          
                    
                    // Lanzar Flask y Wiremock.
                    sh '''
                        n=0
                        flask run &
                        FLASK_PID=$!
                        while ! nc -z localhost 5000; do
                            sleep 1
                            n=$((n+1))
                        done
                        echo "Flask arrancó en $n segundos"
                        n=0
                        java -jar /opt/unir/wiremock-standalone-3.10.0.jar --port 9090 --root-dir test/wiremock &
                        WIREMOCK_PID=$!
                        while ! nc -z localhost 9090; do
                            sleep 1
                            n=$((n+1))
                        done
                        echo "Wiremock arrancó en $n segundos"
                        pytest --junitxml=result-rest.xml test/rest/
                        kill -9 $FLASK_PID
                        kill -9 $WIREMOCK_PID
                    '''
                    
                    // Publicar resultados de las pruebas de integración.
                    junit 'result-rest.xml'
                }    
            }
        }
        // ANÁLISIS ESTÁTICO DEL CÓDIGO (FLAKE8)
        stage('Static') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {  
                    
                    // Ejecutar Flake8 para análisis estático.
                    sh 'flake8 --format=pylint --exit-zero app > flake8.out'
                    
                    // Registrar los resultados de Flake8 y definir quality gates (umbrales de error).
                    recordIssues tools: [flake8(name: 'Flake8', pattern: 'flake8.out')], qualityGates : [
                        [threshold:8, type: 'TOTAL', unstable: true], 
                        [threshold: 10, type: 'TOTAL', unhealthy: true]
                    ]
                }
            }
        }
        // ANÁLISIS DE SEGURIDAD (BANDIT)
        stage('Security') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    
                    // Ejecutar Bandit para análisis de seguridad.
                    sh 'bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}"'
                    
                    // Registrar los resultados de Bandit y definir quality gates.
                    recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], qualityGates : [
                        [threshold:2, type: 'TOTAL', unstable: true], 
                        [threshold: 4, type: 'TOTAL', unstable: false]
                    ]
                }
            }
        }
        // PRUEBAS DE RENDIMIENTO
        stage('Perfomance') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {   
                    
                    // Lanzar Flask y ejecutar jmeter.
                    sh '''
                        n=0
                        flask run &
                        FLASK_PID=$!
                        while ! nc -z localhost 5000; do
                            sleep 1
                            n=$((n+1))
                        done
                        echo "Flask arrancó en $n segundos"
                        /opt/unir/apache-jmeter-5.6.3/bin/jmeter -n -t test/jmeter/flask.jmx -f -l flask.jtl
                        kill -9 $FLASK_PID
                    '''
                    
                    // Generar el informe de rendimiento a partir del archivo JTL de JMeter.
                    perfReport sourceDataFiles: 'flask.jtl'
                }
            }
        }
        // PRUEBAS DE COBERTURA
        stage('Coverage') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {           
                    
                    // Recuperar el archivo de cobertura.
                    unstash 'test-coverage'
                    
                    // Publicar resultados de cobertura.
                    cobertura coberturaReportFile: 'coverage.xml', 
                    conditionalCoverageTargets: '100,0,80', 
                    lineCoverageTargets: '100,0,85' 
                }    
            }
        }   
    }
    // LIMPIAR WORKSPACE
    post {
        always {            
            cleanWs()       
        }
    }
}
