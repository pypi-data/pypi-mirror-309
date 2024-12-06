# C.B.S

CBS adalah alat hacking untuk menjalankan tools apapun ( mendukung semua bahasa program )


# CARA MENGGUNAKANNYA
1. Pertama tama install atau clone reposity ini
   ```bash
   git clone https://github/adjidev/cbs
   ```

   ```bash
   pip install adjidev-cbs
   ```

2. Setelah itu jalankan tools nya
   ```bash
   cbs --help
   ```
   - Untuk melihat versinya
   ```bash
   cbs --version
   ```
   - Untuk wizard ui
   ```bash
   cbs --wizard
   ```



# CARA MENAMBAHKAN PAYLOAD ATAU FITUR BARU

Untuk menambahkan tools atau fitur baru sangatlah gampang anda tinggal menambahkan `cbs_config.xml` seperti ini dibawah ini:

```xml
<cbs_settings>
    <cbs_setting>
        <cmd>sherlock</cmd>
        <description>Temukan username dari berbagai sosial media</description>
        <execute>python sherlock.py</execute>
        <!-- untuk <args> Opsional-->
        <args>--search {args}</args>
        <author>adjidev</author>
        <version>0.0.1</version>
    </cbs_setting>
</cbs_settings>
```

Setelah itu ikuti perintah perintah dibawah ini

```bash
cbs --load "path/ke/folder" --folder "namapayload"
```
- Untuk reposity github
```bash
cbs --load "https://github.com/adjidev/sqlforce"
```

# AKHIR
_Terima kasih sudah membaca ini_

> Disclaimer: jika anda menjual script ini tanpa izin dari saya, saya tidak akan segan segan melaporkan anda ke pihak berwenang