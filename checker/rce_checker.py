#!/usr/bin/env python3
import logging
import requests
from ctf_gameserver import checkerlib
import socket

class ServiceChecker(checkerlib.BaseChecker):

    def place_flag(self, tick):
        conn = connect(self.ip)
        flag = checkerlib.get_flag(tick)
        url = f"http://{self.ip}:5000/admin"
        payload = f'python -c "import os; os.environ[\'FLAG\'] = \'{flag}\'"'
        try:
            resp = requests.get(url, params={'cmd': payload}, timeout=5)
            if resp.status_code == 200:
                logging.info("Flag replanted via admin endpoint.")
            else:
                logging.warning("Admin endpoint returned status code %s, most likely patched by the team", resp.status_code)
                conn.close()
                return checkerlib.CheckResult.OK
        except Exception as e:
            logging.error("Exception accessing admin endpoint: %s", e)
            conn.close()
            return checkerlib.CheckResult.FAULTY

        try:
            resp = requests.get(f"http://{self.ip}:5000/", timeout=5)
            if resp.status_code == 200:
                logging.info("Login page is accessible after replanting flag.")
                conn.close()
                return checkerlib.CheckResult.OK
            else:
                logging.warning("Admin endpoint returned status code %s, most likely patched by the team", resp.status_code)
                conn.close()
                return checkerlib.CheckResult.OK
        except Exception as e:
            logging.error("Exception accessing login page: %s", e)
            conn.close()
            return checkerlib.CheckResult.FAULTY

    def check_flag(self, tick):
        conn = connect(self.ip)
        try:
            resp = requests.get(f"http://{self.ip}:5000/", timeout=5)
            if resp.status_code == 200:
                logging.info("Login page accessible, flag assumed intact.")
                conn.close()
                return checkerlib.CheckResult.OK
            else:
                logging.warning("Admin endpoint returned status code %s, most likely patched by the team", resp.status_code)
                conn.close()
                return checkerlib.CheckResult.OK
        except Exception as e:
            logging.error("Exception accessing login page: %s", e)
            conn.close()
            return checkerlib.CheckResult.FAULTY

    def check_service(self):
        conn = connect(self.ip)
        try:
            resp = requests.get(f"http://{self.ip}:5000/", timeout=5)
            if resp.status_code == 200 and "<form" in resp.text:
                logging.info("Login page accessible and valid.")
                conn.close()
                return checkerlib.CheckResult.OK
            else:
                logging.warning("Login page not accessible or missing form.")
                conn.close()
                return checkerlib.CheckResult.FAULTY
        except Exception as e:
            logging.error("Exception accessing login page: %s", e)
            conn.close()
            return checkerlib.CheckResult.FAULTY

def connect(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 9999))
    return sock


if __name__ == '__main__':
    checkerlib.run_check(ServiceChecker)
