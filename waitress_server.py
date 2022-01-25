# -*- encoding: utf-8 -*-
from waitress import serve
import includes 

serve(includes.app, host='192.168.1.196', port=5000)
