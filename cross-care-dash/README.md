# Dashboard for Cross Care

## To install and run

**Change directory to cross-care-dash**
```bash
cd cross-care-dash
```

**Then run the following commands to install dependencies**
```bash
pip install flask
npm install
```

**To run react server**
```bash
npm run dev
```

**To run flask server**
```bash
python app/tables/data_sort.py
```


## TODO
- Think about disease-drugs table as many to many

- dash processing temporal data
  - pivot current table - columns years, rows diseases, values counts
  - rename for category_time_counts e.g. total_monthly_counts.json
- Frontend
  - add multiselect for diseases, demographics
    - this should be searchable
  - add slider for years in temporal data
- Flask
  - allow disease/demo selection for multiselect
  - allow time selection for temporal data
