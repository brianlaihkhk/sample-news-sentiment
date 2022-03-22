# Coding sample
Coding sample - News sentiment analysis - Submitted by Brian Lai

### Features

- OLAP data structure design
- Support non-AWS setup or AWS setup

- ETL
   - Detect and scan news file. Provide delta / incremental scan feasibility using scanned file.

- Data mining and analysis
   - Text mining, word sentiment mining based on news context
   - Sentiment / metadata aggregation for BI analysis / reporting 

- Analysis visualization
   - Provide popularity, topics, tags for user to select based on their interested area
   - Flexibility on aggregated data roll-up / drill-down based on multiple dimensions (year / month / day / weekday / tag / category / sentiment / topic)
    User is able to search, obtain single piece of news and visualize metadata association

### Framework 

- TextBlob
   - Text-classification ML model : Naive Bayes
   - NN / NNP extractor : Conll Extractor
- sqlAlchemy
- Flask

### Folder

- Sample : Massaged news for ETL (BBC news, check below Remarks)
- ETL : ETL script to extract massaged news, generate metadata, aggregate data for OLAP
- Documentation : Documentation
- Deploy : Deployment script
- News : Backend server for sentiment analysis, UI request handling
- Client : Frontend UI for sentiment analysis
- Tools : Tools for encryption, encoding and local server script for testing
- Setup : Setup script for database initialization

### Prerequsite

- For more details please refer to Documentation folder

- [AWS solution]
   - AWS IAM (Permission setup)
   - AWS VPC (Network connection capability)
   - AWS S3
   - AWS-cli or AWS CloudFormation

   - For this project
      - AWS ECS / AWS EKS (or equivalent for docker hosting)

   - For external BI reports
      - AWS Glue
      - AWS Redshift (For other BI reports integration)

- [non-AWS solution]
   - Docker (for Client + News module)
   - MySQL / Oracle RDBMS (or other SQL database)
   - (Optional) Docker swarm, Kubernetes or equivalent 

### URL request structure

- For further information please refer to Documentation folder

- News
   - /news
   - /news/`category`
   - /news/`category`/`uuid`

- Sentiment
   - /topic
   - /topic/`date`
   - /topic/`date`/`topic`
   - /category
   - /category/`date`
   - /category/`date`/`category`
   - /tag
   - /tag/`date`
   - /tag/`date`/`category`
   - /topic
   - /topic/`date`
   - /topic/`date`/`category`

- Search
   - /search

### Technical Assessment Requirement

- Capture, aggregate news sentiment based on related metadata (topic, keywords, or others)
- Provide suggestions to users by their preferences and interest
- User is able to search, select and navigate news
- Provide roll-up / drill-down capability for metadata
- Logging / documentation and testing are expected as part of the solution.

### Time limit

- 48 hours

### Sample Data
- BBC news dataset : http://mlg.ucd.ie/datasets/bbc.html (by D. Greene and P. Cunningham. "Practical Solutions to the Problem of Diagonal Dominance in Kernel Document Clustering", Proc. ICML 2006.)
- All rights, including copyright, in the content of the original articles are owned by the BBC.

### Remarks
- Using cryptography / cryptocode / simple-crypt will show **invalid elf header** in AWS Lambda (Under osx development). This project will use JWT for configuration encryption and decryption.
- There is no news scraping script included in this project. You can create automated news scraping task using AWS EventBridge or equivalent.
- This project does not provide BI reports for aggregated data navigation and data analysis.
- Regarding to the news source, there are various examples you can find online. For example, you can select all-in-one local news consolidation tools like https://hknews.dev (Source : https://github.com/ayltai/hknews).

### Contact
- Linkedin : https://linkedin.com/in/brianlaihkhk/
- Github : https://github.com/brianlaihkhk/
