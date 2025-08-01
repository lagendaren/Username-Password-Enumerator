# Username & Password Enumerator

A multithreaded Python CLI tool to identify valid usernames and (optionally) valid password combinations on a target login page.

---

## 🚀 Features

- Username enumeration via HTTP POST
- Optional password brute-force for found usernames
- Threaded for speed
- Proxy rotation support
- Customizable delay between requests
- Configurable success detection via keywords
- CLI flags for all key options

---

## 🧪 Requirements

- Python 3.8+
- `requests`

Install dependencies (if needed):

```bash
pip install requests
```

---

## ⚙️ Usage

### 🔍 Basic username scan:

```bash
python username_checker.py -u http://target/login.php -w users.txt
```

### 🔐 Username & password scan:

```bash
python username_checker.py -u http://target/login.php -w users.txt -n passwords.txt --check-passwords
```

### 🧩 Full options:

```bash
python username_checker.py \
  -u http://target/login.php \
  -w users.txt \
  -n passwords.txt \
  --check-passwords \
  --proxies proxies.txt \
  --delay 0.5 \
  --threads 30 \
  --output results.txt \
  --success-words welcome,dashboard,logout
```

---

## 📄 File Formats

### Usernames file (`-w`)

One username per line:

```
admin
user
john
```

### Passwords file (`-n`)

One password per line:

```
123456
password
demo123
```

### Proxies file (`--proxies`)

Each line should be in `IP:PORT` format:

```
1.2.3.4:8080
5.6.7.8:3128
```

---

## 🛡️ Notes

- Use responsibly and only on systems you are authorized to test.
- Over-aggressive settings (low delay, many threads) may get you rate-limited or blocked.
- Headers in the script are designed to mimic browser traffic.

---

## 📌 Default Values

| Flag              | Default                                                                |
| ----------------- | ---------------------------------------------------------------------- |
| `-u`              | `http://lookup.thm/login.php`                                          |
| `-w`              | `/usr/share/seclists/Usernames/Names/names.txt`                        |
| `-n`              | `/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt` |
| `--threads`       | 20                                                                     |
| `--delay`         | 0.0 seconds                                                            |
| `--output`        | `valid_usernames.txt`                                                  |
| `--success-words` | `welcome,dashboard,logout,my account,you are logged in`                |

---

## 📬 Contact

For improvements or questions, open an issue or contact the author.

---

**Disclaimer:** This tool is for educational and authorized use only.

