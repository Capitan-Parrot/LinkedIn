def get_data_from_page(data):
    name = data[5].text
    profession = data[6].text
    company = data[7].text
    city = data[9].text
    return [name, profession, company, city]
