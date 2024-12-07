from MrLou_modules.Certificate_Utils.cert_utils import convert_crt_to_pem, convert_cer_to_pem

# Usage
crt_path = r"C:\Users\LDESCAMP\downloads\DigiCertGlobalRootG2.crt"
pem_path = r"C:\Users\LDESCAMP\downloads\DigiCertGlobalRootG2.pem"
convert_crt_to_pem(crt_path, pem_path)


cer_path = r"C:\Users\LDESCAMP\downloads\Microsoft Azure TLS Issuing CA 01.cer"
pem_path1 = r"C:\Users\LDESCAMP\downloads\Microsoft Azure TLS Issuing CA 01.pem"
convert_cer_to_pem(cer_path, pem_path1)
