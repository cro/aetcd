import socket
import ssl

def retrieve_server_certificate(hostname, port=2379):
    # Create an unverified SSL context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Establish connection and retrieve certificate
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            der_cert = secure_sock.getpeercert(binary_form=True)
    
    # Convert DER format to PEM
    if der_cert:
        return ssl.DER_cert_to_PEM_cert(der_cert)
    return None

if __name__ == "__main__":
    import sys
    target_host = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    certificate = retrieve_server_certificate(target_host)
    print(certificate)

