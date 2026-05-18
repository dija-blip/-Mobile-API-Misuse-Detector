import requests
import random
import time

# =====================================
# CONFIG
# =====================================

URL = "http://localhost:8000/analyze"

# =====================================
# HELPERS
# =====================================

def send_log(data):
    try:
        r = requests.post(URL, json=data)

        print(
            f"[{r.status_code}] "
            f"{data['ip']} -> "
            f"{data['endpoint']} | "
            f"{data['status_code']}"
        )

    except Exception as e:
        print("ERROR:", e)


# =====================================
# NORMAL TRAFFIC
# =====================================

print("\n==============================")
print(" NORMAL TRAFFIC")
print("==============================\n")

normal_endpoints = [
    "/home",
    "/products",
    "/profile",
    "/search",
    "/api/cart",
    "/api/orders",
    "/dashboard"
]

normal_agents = [
    "Mozilla/5.0",
    "Chrome/120",
    "Safari/17",
    "Edge/120"
]

for i in range(50):

    data = {
        "ip": f"192.168.1.{random.randint(1,20)}",
        "method": "GET",
        "endpoint": random.choice(normal_endpoints),
        "status_code": 200,
        "user_agent": random.choice(normal_agents)
    }

    send_log(data)

    time.sleep(0.2)


# =====================================
# ENDPOINT HAMMERING
# =====================================

print("\n==============================")
print(" ENDPOINT HAMMERING")
print("==============================\n")

for i in range(60):

    data = {
        "ip": "5.5.5.5",
        "method": "GET",
        "endpoint": "/admin",
        "status_code": 200,
        "user_agent": "curl"
    }

    send_log(data)

    time.sleep(0.05)


# =====================================
# SQL INJECTION
# =====================================

print("\n==============================")
print(" SQL INJECTION")
print("==============================\n")

for i in range(20):

    data = {
        "ip": "10.10.10.10",
        "method": "GET",
        "endpoint": "/login?id=' OR 1=1 --",
        "status_code": 500,
        "user_agent": "sqlmap"
    }

    send_log(data)

    time.sleep(0.1)


# =====================================
# ENUMERATION ATTACK
# =====================================

print("\n==============================")
print(" ENUMERATION")
print("==============================\n")

for i in range(30):

    data = {
        "ip": "8.8.8.8",
        "method": "GET",
        "endpoint": f"/unknown{i}",
        "status_code": 404,
        "user_agent": "nikto"
    }

    send_log(data)

    time.sleep(0.1)


# =====================================
# BRUTEFORCE ATTACK
# =====================================

print("\n==============================")
print(" BRUTEFORCE")
print("==============================\n")

for i in range(25):

    data = {
        "ip": "172.16.0.5",
        "method": "POST",
        "endpoint": "/api/login",
        "status_code": 401,
        "user_agent": "Mozilla/5.0"
    }

    send_log(data)

    time.sleep(0.1)


# =====================================
# SENSITIVE ENDPOINTS
# =====================================

print("\n==============================")
print(" SENSITIVE ENDPOINTS")
print("==============================\n")

sensitive = [
    "/admin",
    "/debug",
    "/.env",
    "/actuator",
    "/config"
]

for endpoint in sensitive:

    data = {
        "ip": "100.100.100.100",
        "method": "GET",
        "endpoint": endpoint,
        "status_code": 403,
        "user_agent": "python-requests"
    }

    send_log(data)

    time.sleep(0.3)


# =====================================
# PATH TRAVERSAL
# =====================================

print("\n==============================")
print(" PATH TRAVERSAL")
print("==============================\n")

payloads = [
    "/../../etc/passwd",
    "/../../../windows/system32",
    "/../../../../boot.ini"
]

for payload in payloads:

    data = {
        "ip": "200.200.200.200",
        "method": "GET",
        "endpoint": payload,
        "status_code": 500,
        "user_agent": "curl"
    }

    send_log(data)

    time.sleep(0.3)


# =====================================
# BURST TRAFFIC
# =====================================

print("\n==============================")
print(" BURST ATTACK")
print("==============================\n")

for i in range(120):

    data = {
        "ip": "123.123.123.123",
        "method": "GET",
        "endpoint": "/api/products",
        "status_code": 200,
        "user_agent": "Mozilla/5.0"
    }

    send_log(data)


# =====================================
# FINISHED
# =====================================

print("\n==============================")
print(" TEST FINISHED")
print("==============================\n")