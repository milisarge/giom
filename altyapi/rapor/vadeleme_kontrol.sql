select sum(geneltoplam),kdtutar from fatura where fno=(select fno from fatura where inckeyno='@fkod@') group by fno