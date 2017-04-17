pwd
. ./smb.ayar
smbclient -U $smb_sifre //192.168.1.23/zebra -c "print $1" > yazdir.log
