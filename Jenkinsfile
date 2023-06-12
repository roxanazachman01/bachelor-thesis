pipeline {
    agent { 
        node {
            label 'docker-agent-python2'
            }
      }
    triggers {
        pollSCM '* * * * *'
    }
    stages {
        stage('Build') {
            steps {
                echo "Building.."
                sh '''
                echo "doing build stuff.."
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
			cd server
			python3 -m unittest discover -s tests -p "*_test.py"
		'''
            }
        }
        stage('Deliver') {
            steps {
                echo 'Deliver....'
                sh '''
                	python3 server/main.py &
                '''
            }
        }
    }
}