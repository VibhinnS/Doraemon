from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main', methods=['GET','POST'])
def main():
    if request.method == 'POST':
        result = subprocess.run(['python', 'main.py'], capture_output=True, text=True)
        print(result.stdout)
        return render_template('result.html', output=result.stdout)
    else:
        return render_template('index.html')

@app.route('/voice', methods=['GET','POST'])
def voice():
    if request.method == 'POST':
        result = subprocess.run(['python', 'voice_controlled_drone.py'], capture_output=True, text=True)
        print(result.stdout)
        return render_template('result.html', output=result.stdout)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

