#!/usr/bin/env python

# Test:
# http://127.0.0.1:5000/gen/pterodactyl?a=chicken&b=universe

from flask import Flask, request, session, render_template

import subprocess

app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1>Hi!</h1>"

@app.route('/gen/<subj>', methods=['GET', 'POST'])
def gen(subj):
	obj = "cat"
	oop = "block"
	if request.method == 'POST':
		obj = request.form.get('obj', 'DEFAULT')
		oop = request.form.get('oop', 'DEFAULT')
	else:
		obj = request.args.get('a', 'cat') # gets the value of X in http://blah?a=X&b=Y; it 'a' is not found, returns 'cat'
		oop = request.args.get('b', 'block') # gets the value of Y in http://blah?a=X&b=Y; it 'b' is not found, returns 'block'
	return subprocess.check_output(["./cl.sh", subj, obj, oop])

@app.route('/gen_with_write/<subj>', methods=['GET', 'POST'])
def gen_with_file(subj):
	obj = "cat"
	oop = "block"
	if request.method == 'POST':
		obj = request.form['obj']
		oop = request.form['oop']
	else:
		obj = request.args.get('a', 'cat') # gets the value of X in http://blah?a=X&b=Y; it 'a' is not found, returns 'cat'
		oop = request.args.get('b', 'block') # gets the value of Y in http://blah?a=X&b=Y; it 'b' is not found, returns 'block'
	subprocess.check_output(["./clw.sh", subj, obj, oop])
	f = open('out' + '_'.join([subj, obj, oop]) + '.txt')
	res = [line for line in f][0]
	return res

@app.route('/gen/')
def instr():
	return "Make sure you include a '/[subj]' in your URL (e.g. http://.../gen/dog)"

@app.route('/ace/', methods=['POST'])
def ace():
        sig = request.form.get('sig', '')
        rules = request.form.get('rules', '')
	rulefile = request.form.get('rulefile', '')
        blockrules = request.form.get('blockrules', '')
	blockfile = request.form.get('blockfile', '')
        return subprocess.check_output(["./runfol", "-f", sig, "-l", rules, "-r", rulefile, "-b", blockrules, "-x", blockfile])

@app.route('/ace_all/<sig>')
def ace_all(sig):
	subprocess.call(["/home/danf/erg/openproof/runfolold", "-f", sig, "-r", "/home/danf/erg/openproof/rules.all"])
	f = open('/tmp/out.txt')
	res = '<br>'.join([line for line in f])
	return res

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
#    app.run()

