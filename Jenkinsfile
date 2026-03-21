pipeline {
    agent any

    parameters {
        choice(name: 'BUMP_TYPE',
               choices: ['patch', 'minor', 'major'],
               description: 'Version bump type')
    }

    environment {
        GIT_USER_EMAIL = "rohit.sharma@alliedmed.co.in"
        GIT_USER_NAME  = "Rohitsss-lab"
        GIT_REPO_URL   = "https://github.com/Rohitsss-lab/test1.git"
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
                    def currentVersion = readFile('VERSION').trim()
                    echo "Current version: ${currentVersion}"

                    def rawOutput = bat(
                        script: "\"C:\\Program Files\\Python313\\python.exe\" bump_version.py ${params.BUMP_TYPE ?: 'patch'}",
                        returnStdout: true
                    ).trim()

                    echo "Raw bump output: '${rawOutput}'"

                    // Find version number in output — scan from last line upward
                    def lines = rawOutput.split('\n')
                    def newVer = ''
                    for (int i = lines.size() - 1; i >= 0; i--) {
                        def l = lines[i].trim().replaceAll('\r', '')
                        if (l.matches('[0-9]+\\.[0-9]+\\.[0-9]+')) {
                            newVer = l
                            break
                        }
                    }

                    if (!newVer) {
                        error "Could not parse version from: ${rawOutput}"
                    }

                    env.NEW_VERSION = newVer
                    echo "New version: ${env.NEW_VERSION}"
                }
            }
        }

        stage('Commit new version') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-token',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    bat """
                        git config user.email "${GIT_USER_EMAIL}"
                        git config user.name  "${GIT_USER_NAME}"
                        git remote set-url origin https://%GIT_USER%:%GIT_TOKEN%@github.com/Rohitsss-lab/test1.git
                        git add VERSION
                        git commit -m "chore: bump version to v${env.NEW_VERSION} [skip ci]"
                        git tag "v${env.NEW_VERSION}"
                        git push origin main --tags
                    """
                }
            }
        }

        stage('Notify umbrella') {
            steps {
                script {
                    echo "Notifying umbrella → REPO_NAME=test1, REPO_VERSION=${env.NEW_VERSION}"
                }
                build job: 'umbrella-version-tracker',
                      parameters: [
                          string(name: 'REPO_NAME',    value: 'test1'),
                          string(name: 'REPO_VERSION', value: env.NEW_VERSION),
                          string(name: 'BUMP_TYPE',    value: params.BUMP_TYPE ?: 'patch')
                      ],
                      wait: false
            }
        }
    }

    post {
        success { echo "test1 bumped to v${env.NEW_VERSION} successfully!" }
        failure { echo "Pipeline failed for test1" }
    }
}
