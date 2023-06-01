## 📚 Data Explorer API [CKAN Open-D]

---
### ✅ สร้าง Dataset ใน Web UI แบบ Manual ก่อน โดยเลือก Datatype เป็น CSV เพื่อใช้งาน Data Explorer

__ฐานข้อมูลที่เกี่ยวข้อง (schema.table)__

__ชื่อ Dataset ใน DB__ = ckan.resource.[package_id <span style="color:red">(เชื่อมโยงกับ ckan.package.id)</span>]

__ชื่อ Data Explorer ใน DB__ = datastore.[ชื่อ Table จะเป็น Package_ID]

---

__รูปแบบการตั้งชื่อไฟล์__

__resource.package_id__ = <span style="color:red">(a6b) </span><span style="color:blue">(da3) </span><span style="color:#009900">(34-f78a-42dc-81ab-4e934f98c0ac)</span>

__Directory ที่ใช้ในการวางไฟล์ใน Host ตัวอย่าง__

/var/lib/ckan/resources/<span style="color:red">a6b</span>/<span style="color:blue">da3</span>/<span style="color:#009900">34-f78a-42dc-81ab-4e934f98c0ac</span>

🐳 หากใช้งาน Docker ต้องเข้าถึง Volume ใน Path
```/var/lib/docker/volume/<ckan_storage>/_data/resource/bla..```

---
__หากมีการเอาไฟล์ไปวางทับใน Path มีความจำเป็นต้อง Overwrite Data Explorer ในส่วน datastore.[ชื่อ Table จะเป็น Package_ID] ด้วย เนื่องจากไฟล์กับ Data Explorer จะไม่เหมือนกัน__

---
__Data Explorer Columes__

| _id | _full_text | Columes อื่นๆตาม Structure ปกติ |
|-----|------------|---------------------------------|
| 1   | NULL       | bla bla                         |

## 📦 Setup Conda

[Download Miniconda](https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Linux-x86_64.sh)
```bash
chmod +x Miniconda3-py310_23.3.1-0-Linux-x86_64.sh
```
```bash
./Miniconda3-py310_23.3.1-0-Linux-x86_64.sh
```
☑️ Ignore ตามขั้นตอนจนกว่าจะติดตั้งเสร็จ จากนั้นทำการ Source Profile
```bash
source ∼/.bashrc
```
☑️ ติดตั้ง Library ที่ใช้งานใน Script
```py
pip install pandas
pip install psycopg2
pip install numpy
pip install sqlalchemy
pip install urllib
pip install requests
pip install configparser
```
## 📦 Setup Script
☑️ เลือก Path ที่ต้องการวาง ```Script```
```bash
cd /home/softnix
```
☑️ Clone Project
```bash
git clone https://github.com/ezynook/open-data.git
```
☑️ เข้าไปยัง ```directory```
```bash
cd open-data/api
```
☑️ แก้ไขไฟล์ Config ต่างๆ ได้ที่ไฟล์ ```config.ini```
* URL CKAN Database
* ID Dataset (Resource ID) วิธีการดูว่า Resource ID อะไรให้ดูจาก URL เช่น
```http://192.168.10.xx/dataset/xxx/resource/<resource_id>```
```bash
vim config.ini
```
```ini
[MAIN]

USERNAME = "ckan"
PASSWORD = "ckan"
IPADDR = "192.168.10.98"
DB="datastore"
TABLE_ID = "7654c4b2-5ef7-4e93-affe-09acbb06402a"
FILE_PATH = "/var/lib/ckan/resources/765/4c4/"
FILE_NAME = "b2-5ef7-4e93-affe-09acbb06402a"
```
🟢 __ใช้งานแค่เฉพาะ API ให้ใช้ไฟล์__
```py
python api.py
```
🔵 __ใช้งาน API พร้อมกับ Dataset__
```py
python dataset.py
```
✅ __วิธีการนำไปใช้งาน__
* ✈️ Apache Airflow
* ⏱ Linux Crontab

## ✅ วิธีสร้าง Dataset
* สร้างชุดข้อมูลโดยให้เลือกรูปแบบการเก็บข้อมูลเป็น ```CSV``` และกรอกรายละเอียด ```metadata``` ตามปกติให้เรียบร้อย
* เพิ่มทรัพยากรใหม่ โดยให้เลือกนามสกุลของไฟล์เป็น ```CSV``` และทำการ Upload dummy.csv เข้าไปเพื่อเป็นไฟล์จำลอง ให้ระบบสร้าง Resource Table view ให้
* สามารถ Execute Script ให้เป็นข้อมูลปัจจุบันจาก API ได้ทันที


---


> ⚒️ develope by Pasit Y.
