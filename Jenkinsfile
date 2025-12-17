pipeline {
  agent any

  environment {
          NEXUS_CREDENTIALS = credentials('nexus-credentials')
          NEXUS_URL = "http://3.82.209.224:8083"  // replace with your Nexus server URL
      }

  stages {
        stage('Test Nexus Connection') {
            steps {
                script {
                    sh """
                        echo $NEXUS_CREDENTIALS_PSW | docker login $NEXUS_URL -u $NEXUS_CREDENTIALS_USR --password-stdin
                    """
                }
            }
        }
    }
}

