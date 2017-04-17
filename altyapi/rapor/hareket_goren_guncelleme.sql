update tblstsabit AS a
INNER JOIN sthar AS b ON a.stok_kodu = b.stok_kodu
set a.satici_kodu='2501'
WHERE a.satici_kodu = '250x1'
