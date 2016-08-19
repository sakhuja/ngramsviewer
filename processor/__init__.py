from flask import Flask

main_app = Flask(__name__)
main_app.debug = True

import ngram_app