select City.Name from City, Capital, Country where City.Id = Capital.CityId and Capital.CountryCode = Country.Code and Country.Name = "Malaysia";
