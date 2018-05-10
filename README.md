# PACImport
Simple script for generating [PAC Manager](https://en.wikipedia.org/wiki/PACManager) import file.


# Download & Install
```sh
~/projects $ git clone https://github.com/pouriya-jahanbakhsh/PACImport
...
~/projects $ cd PACImport
~/projects/PACImport $ chmod a+x PACImport.py
~/projects/PACImport $ sudo ln -s $PWD/PACImport.py /usr/local/bin/PACImport
~/projects/PACImport $ PACImport -h
Usage: PACImport.py [options]

Options:
  -h, --help            show this help message and exit
  -s START, --start=START
                        Start of range. Should be between 0-254
  -e END, --end=END     End of range. Should be between 1-255
  -b BASE, --base=BASE  Base IP. e.g. 127.0.0
  -f FILENAME, --filename=FILENAME
                        Filename for output data or leave empty for printing
                        data
  -u USER, --user=USER  Host username.
  -p PASSWORD, --password=PASSWORD
                        Host password
  -P PORT, --port=PORT  Host port
```

# Example
I want to generate import file `PACImportFile.yml` with connections for server IPs `192.168.120.1` through `192.168.120.20` for user `root` with password `s3cr3t` on port `22`.  
```sh
~/projects/PACImport $ PACImport -b 192.168.120\
                                 -s 1\
                                 -e 20\
                                 -u root\
                                 -p s3cr3t\
                                 -P 22\
                                 -f PACImportFile.yml
                                 -k /path/to/public/key
~/projects/PACImport $ ls | grep .yml
PACImportFile.yml
```
 In PAC Manager I can import above connections with following steps:  
* Right-click on a connection group.  
* Click on `Import connection(s)...`  
* Find `PACImportFile.yml` and select it.  
* Click `Import`.
