import subprocess
import socket
from datetime import datetime

def run_command(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.DEVNULL)
        return output.decode().strip()
    except subprocess.CalledProcessError:
        return "FAILED"

report = []
report.append(f"Network Health Check Report")
report.append(f"Time: {datetime.now()}")
report.append("-" * 40)

# Checking for IP address
ip_info = run_command(["ip", "a"])
report.append("\n[+] IP Configuration:")
report.append(ip_info.split("\n")[0])

# Checking Gateway
gateway = run_command(["ip", "route"])
report.append("\n[+] Gateway Information:")
report.append(gateway)

# Ping of Gateway
gateway_ip = gateway.split(" ")[2] if "default" in gateway else None
if gateway_ip:
    ping_gateway = run_command(["ping", "-c", "2", gateway_ip])
    report.append("\n[+] Gateway Ping:")
    report.append("Reachable" if ping_gateway != "FAILED" else "Unreachable")

# Internet Connectivity check with Google DNS
internet = run_command(["ping", "-c", "2", "8.8.8.8"])
report.append("\n[+] Internet Connectivity:")
report.append("Working" if internet != "FAILED" else "Not Working")

# DNS Resolution
try:
    socket.gethostbyname("google.com")
    report.append("\n[+] DNS Resolution: Working")
except:
    report.append("\n[+] DNS Resolution: Failed")

# Saving the report
with open("output/report.txt", "w") as f:
    for line in report:
        f.write(line + "\n")

print("\nNetwork health check completed.")
print("Report saved to output/report.txt")
