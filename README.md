# ncpw2bw
Command line conversion tool for migrating from "Nextcloud Passwords" to Bitwarden.  
Author: sausix https://github.com/sausix/ncpw2bw

## Why?
Nextcloud Passwords does not offer any export format which is recognized by Bitwarden.

## Requirements
Python 3 - Only Windows users should have to install it if not already done.  
You may run this script on your server if you are on Windows. You better trust this script :-)


## Usage


### 1. Export passwords
- Login to your Nextcloud instance and move to the Passwords section.
- On the bottom left the third icon should be `Backup & Restore`.
- Choose `Backup/Export`.
- Choose `Prefefined CSV` from the dropdown.
- Optional: Include shared passwords if you have and want.
- Press `Export` button.

The exported CSV file should start with a header like this:
`"Name","Benutzer","Passwort","Notizen","Webseite","Eigene Felder","Ordner","Tags","Favorit","Bearbeitet am","Id","Version","Ordner Id"`  
Yeah! It's localized to your language set in your Nextcloud user settings. Such a stupid decision!  
Should work if you have 13 columns. The column names are ignored.


### 2. Prepare this script
Download convert.py (since it has no dependencies (yet)).  

Know how to run a Python script and skip to **3.** or continue reading:

Depending on your OS you can run convert.py directly only after making the script executable:  
(Unix based): `chmod +x convert.py`

Then run by:  
(Unix based): `./convert.py`

Alternatively you can prepend the Python interpreter:  
(All): `python3 convert.py`

Or specify the full Python path if it's **not** in the PATH variable especially for Windows users:
`C:\Whatever\Path\python3 convert.py [options as below...]`

Apply the call to the commands below appropriately!

### 3. Run convert tool
Simple run method and for double clicky fans:  
`./convert.py` (no arguments)  
Converts a pre placed and expected `passwords_nc_export.csv` in the working directory into `passwords_bw_import.json`.  

Or just specify a source file anywhere and the destination file will be next to it:  
`./convert.py SOURCE_FILE`  
Converts SOURCE_FILE into SOURCE_FILE.json.

Or do it all manually:  
`./convert.py SOURCE_FILE DEST_FILE`  
Converts SOURCE_FILE into DEST_FILE.

Display help as reminder:  
`./convert.py -h`

Existing destinations will be overwritten silently!

### 4. Import
In your Webbrowser import the JSON file into the empty vault.
- Click on the Bitwarden icon
- Click Settings
- Click Vault
- Click Import
- Optional: Select a specific vault and folder
- Choose the first item in the dropdown `Bitwarden (json)` as format.
- Select the JSON file
- Click `Import`

Passwords should be imported and synced to the server immediately. Have fun deleting Nextcloud! :-)


## Restrictions
- Nested folders will be flattened into single folders
- Creation and modification date will be reset to the current time of conversion. Send love or a pull request without exteral depenencies if you would like to preserve the original dates.
- Notes, user fields and tags are merged into the Bitwarden notes field.
- Favorite bookmarks are not marked as favorites anymore. Instead of true/false someone at the Nextcloud Passwords developers decided to export a translated version of the boolean. So it can be "Oui", "Yes", "Nein", etc. Plan is an argument like `--favorite-value=yes` to avoid retranslation.
- Some fields are omitted like: Organization, Collection, FIDO and the password history.
- Definitely contains bugs. Haven't tested all exotic scenes. See:

## Bugs
Submit a friendly reproducible bug report with redacted and minimal password data and I should fix it in time.
