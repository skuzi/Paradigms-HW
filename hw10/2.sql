select Country.Name, LiteracyRate.Rate from Country, LiteracyRate where LiteracyRate.CountryCode = Country.Code group by Country.Name having max(LiteracyRate.Year) = LiteracyRate.Year order by LiteracyRate.Rate desc limit 1;