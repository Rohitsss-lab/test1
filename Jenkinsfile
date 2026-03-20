pipeline {
    agent any

    environment {
        REPO_NAME      = "test1"             // change to "repo2" for second repo
        GIT_USER_EMAIL = "rohit.sharma@alliedmed.co.in"
        GIT_USER_NAME  = "Rohitsss-lab"
        GIT_REPO_URL   = "https://github.com/Rohitsss-lab/test1.git" // change per repo
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-token',
                    url: env.GIT_REPO_URL
            }
        }

        stage('Bump version') {
            steps {
                script {
                    // Read current version before bump
                    def currentVersion = readFile('VERSION').trim()
                    echo "Current version: ${currentVersion}"

                    // Run bump script and capture new version
                    env.NEW_VERSION = sh(
                        script: "python3 bump_version.py patch",
                        returnStdout: true
                    ).trim()

                    echo "New version: ${env.NEW_VERSION}"
                }
            }
        }

        stage('Commit new version') {
            steps {
                sh """
                    git config user.email "${GIT_USER_EMAIL}"
                    git config user.name  "${GIT_USER_NAME}"

                    git add VERSION
                    git commit -m "chore: bump version to v${env.NEW_VERSION} [skip ci]"
                    git tag "v${env.NEW_VERSION}"
                    git push origin main --tags
                """
            }
        }

        stage('Notify umbrella') {
            steps {
                build job: 'umbrella-version-tracker',
                      parameters: [
                          string(name: 'REPO_NAME',    value: env.REPO_NAME),
                          string(name: 'REPO_VERSION', value: env.NEW_VERSION)
                      ],
                      wait: false
            }
        }
    }

    post {
        success {
            echo "${env.REPO_NAME} bumped to v${env.NEW_VERSION} successfully!"
        }
        failure {
            echo "Pipeline failed for ${env.REPO_NAME}"
        }
    }
}
