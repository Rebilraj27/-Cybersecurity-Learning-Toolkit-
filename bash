# Scan your own VM
python cli.py portscan 192.168.56.10 --ports 1-1024

# Check password strength
python cli.py passwd "MyS3cur3P@ss!"

# Crack an MD5 hash (lab only)
python cli.py crack 5f4dcc3b5aa765d61d8327deb882cf99 rockyou.txt --algo md5

# Encrypt / decrypt
python cli.py encrypt "secret message" "mypassword"
python cli.py decrypt "<base64_blob>" "mypassword"

# Web scan (own lab)
python cli.py webscan "http://localhost:8080/?q=test"
