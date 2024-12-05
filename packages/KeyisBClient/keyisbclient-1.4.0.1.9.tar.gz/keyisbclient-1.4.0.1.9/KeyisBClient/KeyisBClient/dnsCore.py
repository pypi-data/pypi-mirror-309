import httpx
import os

ssl_gw_crt_path = os.path.join(os.path.dirname(__file__), 'gw_certs', 'v0.0.1.crt')

class __DNSCore:
    def __init__(self) -> None:
        from KeyisBLogging import logging
        logging.error('\n' + '='*50 +  '\n              CLIENT STARTED\n' + '='*50)
        
        self._connectionAsync = httpx.AsyncClient(verify=ssl_gw_crt_path)
        self._connectionSync = httpx.Client(verify=ssl_gw_crt_path)
        self.hosts = [
                {'host': 'http://51.250.85.38:50000', 'status': 'unknown', 'add_type': 'main'},
                {'host': 'http://api-root-dns.gw.mmbproject.com:50000', 'status': 'unknown', 'add_type': 'main'},
        ]
        self.checkForAnyDNSHosts()
    def checkForAnyDNSHosts(self):
        path = "C:\\GW\\DNS\\hosts.txt"
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if line:
                            self.hosts.append({
                                'host': line,
                                'status': 'unknown',
                                'add_type': 'outFile'
                                })
            except: pass
DNSCore = __DNSCore()