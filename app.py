from flask import Flask, request, abort, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def homepage():
    if request.method == 'POST':
        agentName = request.form.get('agentName')
        choosedButton = request.form.get('choosedButton')
        if choosedButton == 'memberRegisterBtn':
            return redirect(url_for("memberRegisterRequest", agentName=agentName))
        if choosedButton == 'configSettingBtn':
            return 'configSettingBtn'
        if choosedButton == 'reportQueryBtn':
            return 'reportQueryBtn'
    return render_template('amsMenu.html')


@app.route('/in_test_page')
def memberRegisterRequest():
    # return render_template('memberRegisterRequest.html')
    agentName = request.args.get('agentName')
    return render_template('memberRegisterRequest.html', agentName=agentName)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
