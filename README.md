# Coding assessment
Coding assessment - News sentiment - Submitted by Brian Lai

### Features

- News scraping script for news population (local scraping or online schedule scraping)
- Text mining, sentiment mining based on news context
- Provide popularity, topics, tags for user to select based on their interested area
- User are able to roll-up / drill-down based on specific topic or tags (To show information of sudden popularity)
- Machine learning to learn user beheavioral pattern that suggest interested topics / tags
- Support non-AWS setup or AWS setup for your needs

### Framework 

- BeautifulSoup
- scikit-learn
- TextBlob

### Folder

- Scrap : News scraping script
- ETL : ETL script to capture metadata (e.g sentiment), aggregate data
- Documentation : Documentation
- Deploy : Deployment script
- News : Serverless application for support client UI interactions
- Client : reactJs UI for client interactions
- Tools : Tools for encryption, encoding and local server script for testing
- Setup : Setup script for database initialization

### Prerequsite

- For more details please refer to Documentation folder

- [AWS solution]
   - AWS IAM (Permission setup)
   - AWS VPC (Network connection capability)
   - AWS ECS / AWS EKS (or equivalent)
   - AWS S3
   - AWS Glue
   - AWS Redshift
   - AWS-cli or AWS CloudFormation

- [non-AWS solution]
   - Docker
   - MySQL / Oracle RDBMS (or other SQL database for OLAP)
   - (Optional) Docker swarm, Kubernetes or equivalent 

### Technical Assessment Requirement

- Capture, aggregate news based on sentiment, topic, keywords, or other related metadata (e.g popularity)
- Provide suggestions to users by their preferences and interest
- User is able to search, select and up-vote/down-vote news
- [Bonus] Provide roll-up / drill-down capability for metadata
- Logging / documentation and testing are expected as part of the solution.

### Time limit

- 48 hours

### Sample Data
- BBC news dataset : http://mlg.ucd.ie/datasets/bbc.html (by D. Greene and P. Cunningham. "Practical Solutions to the Problem of Diagonal Dominance in Kernel Document Clustering", Proc. ICML 2006.)
- All rights, including copyright, in the content of the original articles are owned by the BBC.

### Remarks
- Using cryptography / cryptocode / simple-crypt will show **invalid elf header** in AWS Lambda (Under osx development). This project will use JWT for configuration encryption and decryption.
- You can use other solutions as data pipeline like AWS EventBridge or equivalent.
- Regarding to the news source, there are various examples you can find online. For example, you can select all-in-one local news consolidation tools like https://hknews.dev (Source : https://github.com/ayltai/hknews with MIT license, but it relies on hosting on AWS as a whole solution) 

### Contact
- Linkedin : https://linkedin.com/in/brianlaihkhk/
- Github : https://github.com/brianlaihkhk/
