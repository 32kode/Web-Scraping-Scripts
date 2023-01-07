# Tools for web scraping

1. Yellow Pages Scraper
   Function takes 2 inputs, type of business and location of business. For example `yellow_pages_scraper('restaurant', 'new_york')`. The script
   Will go through all the businesses on the Yellow pages that fit that description and save them in a dictionary.
   A progress bar is also visible so you know the progress of the scrape.
   
2. DecisionMakerTool:

This tool is used to fetch decision makers information from Finnish companies. 
The tool takes finnish company IDs and exports the decision maker names as well as positions in the company.
(import txt file with companyIDs, export excel file with a table containing (companyID, name, position))
Backend code of this tool works as intended but the front end refinment is still a work in progress.
Version 1.0
indepth_company_scrape: scrape wide info about a company
  
3. Finnish Company Data scraper
   Input a .txt with company-ID:s and export a Excel with scraped data, 
   The outputted Excel includes:
   
   - Y-tunnus (Business ID)
   - Perustusvuosi (Foundation year)
   - Toimitusjohtaja (CEO)
   - Sähköposti (Email address)
   - Puhelin (Phone number)
   - Verkkosivut (Website)
   - Kotipaikka (Home location)
   - Käyntiosoite (Physical address)
   - Postiosoite (Postal address)
   - Päätoimiala (Main industry)
   - Yhtiömuoto (Company form)
   - Liikevaihto 2022 (Revenue in 2022)
