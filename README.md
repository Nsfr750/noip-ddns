# No-IP DDNS Manager

**Gestione e aggiornamento IP dinamico su no-ip.com**

**Manage and update dynamic IP on no-ip.com**

  Copyright 2024-2026 Nsfr750 - All rights reserved.

---

## Description / Descrizione

**English:**
No-IP DDNS Manager is an application for automatic management of dynamic IP updates on no-ip.com. The application monitors your public IP and automatically updates configured DNS records when the IP changes.

**Italiano:**
No-IP DDNS Manager è un'applicazione per la gestione automatica dell'aggiornamento IP dinamico su no-ip.com. L'applicazione monitora il tuo IP pubblico e aggiorna automaticamente i record DNS configurati quando l'IP cambia.

---

## Features / Caratteristiche

- **Automatic DDNS update on no-ip.com** / Aggiornamento automatico DDNS su no-ip.com
- **Modern and responsive web interface** / Interfaccia web moderna e responsive
- **Secure credential management** / Gestione sicura delle credenziali
- **Detailed operation logs** / Log dettagliati delle operazioni
- **Multi-host configuration** / Configurazione multi-host
- **On-demand manual update** / Aggiornamento manuale on-demand
- **Mobile-friendly interface** / Interfaccia mobile-friendly

---

## Requirements / Requisiti

- **ASUSTOR/Synology NAS with APK support** / ASUSTOR/Synology NAS con supporto APK
- **Python 3.x**
- **Active internet connection** / Connessione internet attiva
- **no-ip.com account** / Account no-ip.com

---

## Installation / Installazione

**English:**
1. Download the APK package file
2. Install the package through your NAS application center
3. Access the web interface at `http://<nas-ip>:7777`
4. Configure your no-ip.com hosts

**Italiano:**
1. Scarica il file APK del pacchetto
2. Installa il pacchetto tramite il centro applicazioni del tuo NAS
3. Accedi all'interfaccia web all'indirizzo `http://<nas-ip>:7777`
4. Configura i tuoi host no-ip.com

---

## Configuration / Configurazione

### Via Web Interface / Tramite Interfaccia Web

**English:**
1. Access the web interface
2. In the "Configured Hosts" section, enter:
   - **Hostname**: Your no-ip.com domain (e.g., `mydomain.ddns.net`)
   - **Username**: Your no-ip.com username
   - **Password**: Your no-ip.com password
3. Click "Add Host"
4. Repeat for all hosts you want to manage

**Italiano:**
1. Accedi all'interfaccia web
2. Nella sezione "Host Configurati", inserisci:
   - **Hostname**: Il tuo dominio no-ip.com (es. `miodominio.ddns.net`)
   - **Username**: Il tuo username no-ip.com
   - **Password**: La tua password no-ip.com
3. Clicca su "Aggiungi Host"
4. Ripeti per tutti gli host che desideri gestire

### Via Configuration File / Tramite File di Configurazione

**English:**
The configuration file is located at `/usr/local/AppCentral/noip-ddns/etc/config.json`:

**Italiano:**
Il file di configurazione si trova in `/usr/local/AppCentral/noip-ddns/etc/config.json`:

```json
{
  "hosts": [
    {
      "hostname": "example.ddns.net",
      "username": "your_username",
      "password": "your_password"
    }
  ],
  "update_interval": 300,
  "last_update": null,
  "last_ip": null
}
```

---

## Usage / Utilizzo

### Automatic Update / Aggiornamento Automatico

**English:**
The DDNS service starts automatically upon installation and checks the public IP every 5 minutes (300 seconds). If the IP changes, it automatically updates all configured hosts.

**Italiano:**
Il servizio DDNS viene avviato automaticamente all'installazione e controlla l'IP pubblico ogni 5 minuti (300 secondi). Se l'IP cambia, aggiorna automaticamente tutti gli host configurati.

### Manual Update / Aggiornamento Manuale

**English:**
From the web interface, you can force an immediate update by clicking the " Update" button next to each host.

**Italiano:**
Dall'interfaccia web, puoi forzare un aggiornamento immediato cliccando sul pulsante " Aggiorna" accanto a ciascun host.

### Viewing Logs / Visualizzazione Log

**English:**
Operation logs are available in the web interface "Logs" section and are saved to `/var/log/noip-ddns.log`.

**Italiano:**
I log delle operazioni sono disponibili nell'interfaccia web nella sezione "Log" e vengono salvati in `/var/log/noip-ddns.log`.

---

## Package Structure / Struttura del Pacchetto

```text
noip-ddns/
├── control/
│   ├── config.json          # Package configuration / Configurazione pacchetto
│   ├── description.txt      # Description / Descrizione
│   ├── changelog.txt        # Changelog
│   ├── icon.png             # Package icon / Icona del pacchetto
│   ├── icon-disable.png     # Disabled package icon / Icona disabilitata del pacchetto
│   ├── icon-enable.png      # Enabled package icon / Icona abilitata del pacchetto
│   ├── start-stop.sh        # Start/stop script / Script avvio/arresto
│   ├── pre-install.sh       # Pre-install script / Script pre-installazione
│   ├── post-install.sh      # Post-install script / Script post-installazione
│   ├── pre-uninstall.sh     # Pre-uninstall script / Script pre-disinstallazione
│   └── post-uninstall.sh    # Post-uninstall script / Script post-disinstallazione
└── data/
    ├── lib/
    │   └── ddns_updater.py  # Python DDNS update script / Script Python aggiornamento DDNS
    ├── etc/
    │   └── config.json      # Configuration file / File configurazione
    └── webapp/
        └── index.html       # Web interface / Interfaccia web
```

---

## Commands / Comandi

### Start Service / Avvio del Servizio

```bash
/usr/local/AppCentral/noip-ddns/control/start-stop.sh start
```

### Stop Service / Arresto del Servizio

```bash
/usr/local/AppCentral/noip-ddns/control/start-stop.sh stop
```

### Manual Update / Aggiornamento Manuale

```bash
/usr/local/bin/python3 /usr/local/AppCentral/noip-ddns/lib/ddns_updater.py --once
```

### Run as Daemon / Esecuzione come Daemon

```bash
/usr/local/bin/python3 /usr/local/AppCentral/noip-ddns/lib/ddns_updater.py --daemon --interval 300
```

---

## Troubleshooting / Risoluzione Problemi

### Service Won't Start / Il servizio non si avvia

**English:**
1. Check logs in `/var/log/noip-ddns.log`
2. Verify Python 3 is installed: `/usr/local/bin/python3 --version`
3. Ensure ports are not in use

**Italiano:**
1. Controlla i log in `/var/log/noip-ddns.log`
2. Verifica che Python 3 sia installato: `/usr/local/bin/python3 --version`
3. Assicurati che le porte non siano in uso

### IP Not Updating / L'IP non viene aggiornato

**English:**
1. Verify no-ip.com credentials
2. Check hostname is correct
3. Verify internet connection
4. Check logs for specific errors

**Italiano:**
1. Verifica le credenziali no-ip.com
2. Controlla che l'hostname sia corretto
3. Verifica la connessione internet
4. Controlla i log per errori specifici

### no-ip.com Authentication Error / Errore di autenticazione no-ip.com

**English:**
1. Verify username and password
2. Ensure you're using no-ip.com credentials (not email)
3. Check account is active

**Italiano:**
1. Verifica username e password
2. Assicurati di usare le credenziali no-ip.com (non email)
3. Controlla che l'account sia attivo

---

## Security / Sicurezza

**English:**
- Passwords are stored in plain text in the configuration file
- Ensure `config.json` has restrictive permissions
- Use strong passwords for your no-ip.com account
- Consider using a dedicated account for DDNS

**Italiano:**
- Le password sono salvate in chiaro nel file di configurazione
- Assicurati che il file `config.json` abbia permessi restrictivi
- Usa password complesse per l'account no-ip.com
- Considera l'uso di un account dedicato per DDNS

---

## License / Licenza

**English:**
This project is distributed under GPLv3 license.

**Italiano:**
Questo progetto è distribuito sotto licenza GPLv3.

---

## Support / Supporto

**English:**
For issues or questions:
- Email: [Nsfr750](mailto:nsfr750@yandex.com)
- Website: https://www.tuxxle.org
- GitHub: https://github.com/Nsfr750

**Italiano:**
Per problemi o domande:
- Email: [Nsfr750](mailto:nsfr750@yandex.com)
- Sito web: https://www.tuxxle.org
- GitHub: https://github.com/Nsfr750

---

## Developer / Sviluppatore

- **Organization / Organizzazione**: Tuxxle
- **Developer / Sviluppatore**: Nsfr750
- **Year / Anno**: 2024-2026

---

## Acknowledgments / Ringraziamenti

**English:**
Thanks to no-ip.com for the DDNS service.

**Italiano:**
Grazie a no-ip.com per il servizio DDNS.
