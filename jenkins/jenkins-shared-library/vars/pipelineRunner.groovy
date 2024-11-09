def check() {
    node('built-in'){
        deleteDir()
        echo "hello check pipeline!"
    }
}

def gate() {
    node('built-in'){
        deleteDir()
        echo "hello gate pipeline!"
    }
}

def post() {
    node('built-in'){
        deleteDir()
        echo "hello post pipeline!"
    }
}

def trigger() {
    node('built-in'){
        deleteDir()
        echo "hello trigger pipeline!"
    }
}
