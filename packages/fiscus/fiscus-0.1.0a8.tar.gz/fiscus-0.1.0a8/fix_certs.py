import ssl
import certifi
import subprocess
import urllib.request
from pathlib import Path

# Step 1: Retrieve the server's certificate chain
def fetch_certificate_chain(server_url, output_file="server_cert_chain.pem"):
    print(f"[INFO] Fetching certificate chain from {server_url}...")
    try:
        command = [
            "openssl", "s_client", "-connect", server_url, "-showcerts"
        ]
        with open(output_file, "w") as f:
            subprocess.run(command, stdout=f, stderr=subprocess.PIPE, input="Q", text=True)
        print(f"[INFO] Certificate chain saved to {output_file}.")
    except Exception as e:
        print(f"[ERROR] Failed to fetch certificate chain: {e}")

# Step 2: Extract certificates from the chain
def extract_certificates(chain_file):
    print(f"[INFO] Extracting certificates from {chain_file}...")
    with open(chain_file, "r") as f:
        chain_content = f.read()

    certs = chain_content.split("-----END CERTIFICATE-----")
    cert_files = []
    for i, cert in enumerate(certs):
        cert = cert.strip()
        if cert:
            cert += "\n-----END CERTIFICATE-----\n"
            output_file = f"cert_{i + 1}.pem"
            with open(output_file, "w") as cert_file:
                cert_file.write(cert)
            cert_files.append(output_file)
            print(f"[INFO] Certificate {i + 1} saved to {output_file}.")
    return cert_files

# Step 3: Append certificates to the certifi CA bundle
def append_to_certifi(cert_files):
    certifi_path = certifi.where()
    print(f"[INFO] Appending certificates to certifi CA bundle: {certifi_path}...")
    with open(certifi_path, "a") as f:
        for cert_file in cert_files:
            with open(cert_file, "r") as cf:
                f.write(cf.read())
    print("[INFO] Certificates appended to certifi CA bundle.")

# Step 4: Verify the updated certificate chain
def verify_chain(cert_files):
    certifi_path = certifi.where()
    for cert_file in cert_files:
        print(f"[INFO] Verifying {cert_file} with certifi bundle...")
        result = subprocess.run(
            ["openssl", "verify", "-CAfile", certifi_path, cert_file],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        print(f"[RESULT] {result.stdout.strip()}")
        if result.returncode != 0:
            print(f"[ERROR] Verification failed for {cert_file}: {result.stderr.strip()}")

# Step 5: Test HTTPS request with the updated CA bundle
def test_https_request(url):
    print(f"[INFO] Testing HTTPS request to {url}...")
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        with urllib.request.urlopen(url, context=context) as response:
            print(f"[INFO] HTTPS request successful! Status code: {response.status}")
            print(response.read().decode("utf-8"))
    except Exception as e:
        print(f"[ERROR] HTTPS request failed: {e}")

# Main function to execute all steps
def main():
    server_url = "5qva06rx59.execute-api.us-east-1.amazonaws.com:443"
    test_url = "https://5qva06rx59.execute-api.us-east-1.amazonaws.com/prod/execute"

    chain_file = "server_cert_chain.pem"

    # Fetch, extract, and append certificates
    fetch_certificate_chain(server_url, chain_file)
    cert_files = extract_certificates(chain_file)
    append_to_certifi(cert_files)

    # Verify the updated chain and test HTTPS
    verify_chain(cert_files)
    test_https_request(test_url)

if __name__ == "__main__":
    main()
