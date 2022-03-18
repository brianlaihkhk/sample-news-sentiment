# Coding assessment
Coding assessment - News sentiment - Submitted by Brian Lai

### Features

- News scraping script for news population (local scraping or online schedule scraping)
- Text mining, sentiment learning based on news context
- Provide popularity, topics, tags for user to select based on their interested area
- User are able to roll-up / drill-down based on specific topic or tags (To show information of sudden popularity)
- Machine learning to learn user beheavioral pattern that suggest interested topics / tags

### Framework 

- BeautifulSoup
- PyTorch
- TextBlob

### Folder

- ETL : ETL script to capture metadata (e.g sentiment), aggregate data
- Documentation : Documentation
- Deploy : Deployment script
- News : Serverless application for support client UI interactions
- Client : reactJs UI for client interactions
- Tools : Tools for encryption, encoding and local server script for testing

### Prerequsite

- AWS IAM setup with AWS Lambda deployment capability
- AWS VPC setup that AWS Lambda is able to connect to public and to AWS RDS MySQL 
- Serverless framework for AWS Lambda deployment

### Technical Assessment Requirement

- Capture, aggrate news based on sentiment, topic, keywords, or other related metadata (e.g popularity)
- Provide suggestions to users by their preferences and interest
- User is able to search, select and up-vote/down-vote news
- [Bonus] Provide roll-up / drill-down capability for metadata
- Logging / documentation and testing are expected as part of the solution.

### Time limit

- 48 hours

### Contact
- Linkedin : https://linkedin.com/in/brianlaihkhk/
- Github : https://github.com/brianlaihkhk/
