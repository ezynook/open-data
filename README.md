# วิธีการติดตั้ง CKAN Open-Data

---
### Download CKAN Open-Data
```bash
$ cd /home/
$ git clone https://github.com/ezynook/open-data.git
$ cd open-data/
```
### Environment
PostgreSQL Database

```db: ckan | username: ckan password: ckan```

สามารถแก้ไข IP Address และ Port ได้ที่ไฟล์ .env

```bash
$ vim .env

PORT=8080
IPADDR=192.168.10.47
```

### Start Container
```bash
$ docker-compose up -d
```
### Start Browser
```bash
http://<ip address>:<port>
#Default admin username/password
Username: admin
Password: password
```