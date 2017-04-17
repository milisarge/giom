SELECT SUM( MIKTAR )
FROM sthar
WHERE FTIP = 'C'
AND KAYNAK = '@merkez@'
AND STOK_KODU = '@stokod@'
AND TARIH >= DATE_SUB( CURDATE( ) , INTERVAL @gerigun@ DAY ) 
