#! /usr/bin/python

from uuid import uuid4


class PACImport:

	def __init__(self
	            ,base_ip="127.0.0"
	            ,filename="PACImport.yml"
	            ,_range=(0, 255)
	            ,user=""
	            ,password=""
	            ,port=22):
		count = 0
		for octet in base_ip.split("."):
			if (count > 3) or (not octet.isdigit()) or (int(octet) < 0) or (int(octet) > 255):
				raise ValueError("base_ip: {}".format(base_ip))
			count += 1
		else:
			if count != 3:
				raise ValueError("base_ip: {}".format(base_ip))

		start, stop = _range
		if start < 0 or start > 254:
			raise ValueError("start: {}".format(start))
		if stop == 0 or stop > 255:
			raise ValueError("stop: {}".format(stop))

		if not user:
			raise ValueError("empty user")

		self.base_ip = base_ip
		self.filename = filename
		self.start, self.stop = _range
		self.user = user
		self.password = password
		self.port = port


	def make_connection(self, uuid, ip, user, password, port):
		return """{uuid}:
  KPX title regexp: .*{ip}.*
  _is_group: 0
  _protected: 0
  auth fallback: 1
  auth type: userpass
  autoreconnect: ''
  autossh: ''
  children: {{}}
  cluster: []
  description: Connection with '{ip}'
  embed: 0
  expect: []
  favourite: 0
  infer from KPX where: 3
  infer user pass from KPX: ''
  ip: 192.168.95.180
  local after: []
  local before: []
  local connected: []
  mac: ''
  macros: []
  method: SSH
  name: {ip}
  options: ' -X'
  parent: __PAC__EXPORTED__
  pass: '{password}'
  passphrase: ''
  passphrase user: ''
  port: {port}
  prepend command: ''
  proxy ip: ''
  proxy pass: ''
  proxy port: 8080
  proxy user: ''
  public key: ~
  quote command: ''
  remove control chars: ''
  save session logs: ''
  screenshots: ~
  search pass on KPX: 0
  send slow: 0
  send string active: ''
  send string every: 60
  send string intro: 1
  send string txt: ''
  session log pattern: <UUID>_<NAME>_<DATE_Y><DATE_M><DATE_D>_<TIME_H><TIME_M><TIME_S>.txt
  session logs amount: 10
  session logs folder: ~/.config/pac/session_logs
  startup launch: ''
  startup script: ''
  startup script name: sample1.pl
  terminal options:
    audible bell: ''
    back color: '#000000000000'
    bold color: '#cc62cc62cc62'
    bold color like text: 1
    command prompt: '[#%\$>]|\:\/\s*$'
    cursor shape: block
    disable ALT key bindings: ''
    disable CTRL key bindings: ''
    disable SHIFT key bindings: ''
    open in tab: 1
    password prompt: "([p|P]ass|[p|P]ass[w|W]or[d|t]|ontrase.a|Enter passphrase for key '.+'):\\\s*$"
    tab back color: '#000000000000'
    terminal backspace: auto
    terminal character encoding: UTF-8
    terminal emulation: xterm
    terminal font: Monospace 9
    terminal scrollback lines: 5000
    terminal select words: \.:_\/-A-Za-z0-9
    terminal transparency: 0
    terminal window hsize: 800
    terminal window vsize: 600
    text color: '#cc62cc62cc62'
    timeout command: 40
    timeout connect: 40
    use personal settings: ''
    use tab back color: ''
    username prompt: '([l|L]ogin|[u|u]suario|[u|U]ser-?[n|N]ame|[u|U]ser):\s*$'
    visible bell: ''
  title: {ip}
  use prepend command: ''
  use proxy: 0
  use sudo: ''
  user: {user}
  variables: []""".format(uuid=uuid, ip=ip, user=user, password=password, port=port)


	def main(self):
		header = "---\n__PAC__EXPORTED__:\n  children:\n"
		connections = ""
		for octet in range(self.start, self.stop):
			uuid = uuid4()
			header += "    {}: 1\n".format(uuid)
			ip = self.base_ip + "." + str(octet)
			connections += self.make_connection(uuid
			                                   ,ip
			                                   ,self.user
			                                   ,self.password
			                                   ,self.port) + "\n"
		data = header + connections
		if self.filename:
			fd = open(self.filename, "w")
			fd.write(data)
			fd.close()
		else:
			print(data)

if __name__ == "__main__":
	from optparse import OptionParser

	optp = OptionParser()
	optp.add_option("-s"
	               ,"--start"
	               ,dest="start"
	               ,help="Start of range. Should be between 0-254"
	               ,default=0
	               ,type="int")
	optp.add_option("-e"
	               ,"--end"
	               ,dest="end"
	               ,help="End of range. Should be between 1-255"
	               ,default=255
	               ,type="int")
	optp.add_option("-b"
	               ,"--base"
	               ,dest="base"
	               ,help="Base IP. e.g. 127.0.0"
	               ,default="127.0.0"
	               ,type="str")
	optp.add_option("-f"
	               ,"--filename"
	               ,dest="filename"
	               ,help="Filename for output data or leave empty for printing data"
	               ,default=""
	               ,type="str")
	optp.add_option("-u"
	               ,"--user"
	               ,dest="user"
	               ,help="Host username."
	               ,default="root"
	               ,type="str")
	optp.add_option("-p"
	               ,"--password"
	               ,dest="password"
	               ,help="Host password"
	               ,default=""
	               ,type="str")
	optp.add_option("-P"
	               ,"--port"
	               ,dest="port"
	               ,help="Host port"
	               ,default=22
	               ,type="int")
	opts, args = optp.parse_args()

	PACImport(opts.base
	         ,opts.filename
	         ,(opts.start, opts.end)
	         ,opts.user
	         ,opts.password
	         ,opts.port).main()
