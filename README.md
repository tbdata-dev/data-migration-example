# Data Migration Example

- Handles the heavy lifting of data cleaning and transformation in a  service layer
- Separates logic by data type (companies, contacts, deals, etc.) for clarity and maintainability
- Uses small utility functions for things like logging, file handling, and formatting
- Log file contains full data load, all queries, and pre and post normalized data on a row by row basis
- Stores the processed data in a relational database (SQLite) for querying and validation
- Outputs final db data to csv files
### Repo Layout
```
data-migration-example/
├── data/                         # Input/output file storage
│   ├── final_files/             # Final CSVs after processing
│   └── original_files/          # Raw data files for ingestion
│
├── models/                      # SQLAlchemy models for database schema
│   ├── base.py
│   ├── companies.py
│   ├── contacts.py
│   ├── deals.py
│   └── marketing_participants.py
│
├── services/                    # ETL logic grouped by entity
│   ├── companies/               # Company logic
│   │   ├── pe_comps.py
│   │   ├── pipelines.py
│   │   ├── process_companies.py
│   │   └── shared.py
│   ├── contacts/                # Contact logic
│   │   ├── contacts.py
│   │   ├── events.py
│   │   ├── pe_comps.py
│   │   ├── pipelines.py
│   │   ├── process_contacts.py
│   │   └── shared.py
│   ├── deals/                   # Deal logic
│   │   ├── pipelines.py
│   │   ├── process_deals.py
│   │   └── shared.py
│   ├── marketing_participants/ # Marketing participants logic
│       ├── events.py
│       ├── process_marketing_participants.py
│       └── shared.py
│   └── export_data_to_csv.py       # Output exporter for processed data
├── utils/                       # Shared utilities (logging, file I/O)
│   ├── data.py
│   ├── file.py
│   └── logger.py
│
├── tests/                       # Test scripts and validation
│   └── scrap.py
│
├── main.py                      # Entrypoint to run ETL pipeline
├── example.db                   # SQLite DB 
├── data_load.log                # Log file
├── docs.txt                     # Documentation notes
├── requirements.txt             # Python dependency list
├── .gitignore
└── README.md