def runScript(String file, String param='') {
    def cmd = libraryResource file
    if (param){
        def exe_file = UUID.randomUUID().toString() + '.sh'
        writeFile file: exe_file, text: cmd.stripIndent()
        cmd = "chmod a+x ${exe_file}; ./${exe_file} ${param}; rm -f ${exe_file};"
        return sh (script: cmd, returnStdout: true).trim()
    }else{
        sh script: cmd.stripIndent()
    }
}
