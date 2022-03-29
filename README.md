# Coding sample
Coding sample - News sentiment BI analysis - Submitted by Brian Lai

### Features

- OLAP data structure design
- Support non-AWS setup or AWS setup

- ETL
   - Detect and scan news file
   - Provide delta / incremental scan feasibility using scanned file

- Data mining and analysis
   - Text mining, word sentiment mining based on news context
   - Sentiment / metadata aggregation for BI analysis / reporting 

- BI analysis visualization
   - Provide sentiment, topics, tags for user to select based on their interested area
   - Flexibility on aggregated data roll-up / drill-down based on multiple dimensions ( year / month / day / weekday / tag / category / sentiment / topic )
   - User is able to search, obtain single piece of news and visualize metadata association

### Framework 

- [ETL (Sentiment extraction)]
   - TextBlob
      - Text-classification ML algorithm : Naive Bayes
      - NN / NNP extractor : Conll Extractor
   - sqlAlchemy
   - boto3
   - unittest

- [Client (BI report UI)]
   - native-script for jest
   - babel / eslint for jsx

- [News (BI reporting server)]
   - sqlAlchemy
   - Flask
   - unittest

### Folder

- Sample : Massaged news for ETL (BBC news, check below Remarks)
- ETL : ETL script to extract massaged news, generate metadata, aggregate data for OLAP
- Deploy : Deployment script
- News : Reporting engine for Client UI
- Client : UI for sentiment analysis
- Unit Test : Unit testing script
- Tools : Tools for encryption, encoding and local server script for testing
- Setup : Setup script for database initialization
- Documentation : Documentation
- Screenshot : Application screenshots

### Prerequsite

- For more details please refer to Documentation folder

- [AWS solution]
   - AWS IAM (Permission setup)
   - AWS VPC (Network connection capability)
   - AWS S3
   - AWS-cli or AWS CloudFormation
   - npm, pip3

   - [using SQL as OLAP]
      - AWS Lambda (ETL script)
      - AWS CloudWatch (AWS Lambda schedule job)
      - AWS RDS MySQL (or equivalent for OLAP)
      - AWS ECS or EKS (News reporting server)
      - Serverless (Deployment of lambda script)

   - [using Data warehouse as OLAP]
      - AWS Glue (MySQL / RDBMS -> Redshift)
      - AWS Redshift (Data warehouse)
      - AWS Quicksight (or equivalent for other BI reporting)

- [non-AWS solution]
   - Docker (for News reporting server)
   - npm, pip3
   - MySQL / Oracle RDBMS (or equivalent for OLAP)
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
   - /tag/`date`/`tag`
   - /sentiment
   - /sentiment/`date`
   - /sentiment/`date`/`sentiment`

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
- Regarding to the news source, there are various examples you can find online. For example, you can select all-in-one local news consolidation tools like https://hknews.dev (Source : https://github.com/ayltai/hknews) 

### Contact
- Linkedin : https://linkedin.com/in/brianlaihkhk/
- Github : https://github.com/brianlaihkhk/
