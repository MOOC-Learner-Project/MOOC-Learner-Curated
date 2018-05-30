#!/usr/bin/env groovy

node {
    stage('Setup Configuration') {
        properties([pipelineTriggers([[$class: 'GitHubPushTrigger']])])
    }
    stage('Run Unittests') {
        checkout scm
        sh 'cd ${WORKSPACE}'
        sh 'sudo mkdir .unittest_report || true'
        sh 'sudo python2 /usr/local/bin/nosetests --with-xunit --xunit-file=.unittest_report/index.xml || true'
        sh 'sudo xsltproc -o .unittest_report/index.html .unittest_report/style.xslt .unittest_report/index.xml || true'
        sh 'sudo python2 /usr/local/bin/nosetests --with-coverage --cover-html --cover-html-dir=.coverage_report || true'
        sh 'sudo coverage xml || true'
    }
    stage('Archive Reports') {
        archiveArtifacts artifacts: '.coverage_report/*.*', fingerprint: true
        archiveArtifacts artifacts: '.unittest_report/*.*', fingerprint: true
        archiveArtifacts artifacts: 'coverage.xml', fingerprint: true
        archiveArtifacts artifacts: '.coveragerc', fingerprint: true        
    }
    stage('Publish Reports') {
        publishHTML (target: [
            allowMissing: false,
            alwaysLinkToLastBuild: false,
            keepAll: false,
            reportDir: '.unittest_report',
            reportFiles: 'index.html',
            reportName: 'Unittest Report',
            reportTitles: 'Unittest Report'
        ])
        publishHTML (target: [
            allowMissing: false,
            alwaysLinkToLastBuild: false,
            keepAll: false,
            reportDir: '.coverage_report',
            reportFiles: 'index.html',
            reportName: 'Coverage Report',
            reportTitles: 'Coverage Report'
        ])
    }
    stage('Publich Build and Coverage Status') {
        /*
        currentBuild.result = 'SUCCESS'
        step([$class: 'MasterCoverageAction'])
        step([$class: 'CompareCoverageAction'])
        */
    }
}