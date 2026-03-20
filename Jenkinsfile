pipeline {
    agent any

    stages {

        stage('Read version') {
            steps {
                script {
                    env.REPO_VERSION = readFile('VERSION').trim()
                    echo "Repo 1 version: ${env.REPO_VERSION}"
                }
            }
        }

        stage('Notify umbrella') {
            steps {
                // Trigger the umbrella pipeline and pass repo name + version
                build job: 'umbrella-version-tracker',
                      parameters: [
                          string(name: 'REPO_NAME',    value: 'repo1'),
                          string(name: 'REPO_VERSION', value: env.REPO_VERSION)
                      ],
                      wait: false
            }
        }
    }
}
