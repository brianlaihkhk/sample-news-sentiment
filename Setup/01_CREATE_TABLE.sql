USE NEWS;

CREATE TABLE IF NOT EXISTS AGGREGATE_CATEGORY (
   NEWS_DAY             VARCHAR(8) NOT NULL,
   SORT_YEAR                 VARCHAR(4) NOT NULL,
   SORT_MONTH                VARCHAR(2) NOT NULL,
   SORT_DAY                  VARCHAR(2) NOT NULL,
   DAY_OF_WEEK          VARCHAR(3) NOT NULL,
   CATEGORY             VARCHAR(30) NOT NULL,
   NEWS_COUNT           INT NOT NULL,
   POPULARITY           INT NOT NULL,
   PRIMARY KEY ( NEWS_DAY, CATEGORY ),
   INDEX ( DAY_OF_WEEK, CATEGORY ),
   INDEX ( CATEGORY )
);

CREATE TABLE IF NOT EXISTS AGGREGATE_SENTIMENT (
   NEWS_DAY             VARCHAR(8) NOT NULL,
   SORT_YEAR                 VARCHAR(4) NOT NULL,
   SORT_MONTH                VARCHAR(2) NOT NULL,
   SORT_DAY                  VARCHAR(2) NOT NULL,
   DAY_OF_WEEK          VARCHAR(3) NOT NULL,
   SENTIMENT             VARCHAR(30) NOT NULL,
   NEWS_COUNT           INT NOT NULL,
   POPULARITY           INT NOT NULL,
   PRIMARY KEY ( NEWS_DAY, SENTIMENT ),
   INDEX ( DAY_OF_WEEK, SENTIMENT ),
   INDEX ( SENTIMENT )
);

CREATE TABLE IF NOT EXISTS AGGREGATE_TOPIC (
   NEWS_DAY             VARCHAR(8) NOT NULL,
   SORT_YEAR                 VARCHAR(4) NOT NULL,
   SORT_MONTH                VARCHAR(2) NOT NULL,
   SORT_DAY                  VARCHAR(2) NOT NULL,
   DAY_OF_WEEK          VARCHAR(3) NOT NULL,
   TOPIC             VARCHAR(100) NOT NULL,
   NEWS_COUNT           INT NOT NULL,
   POPULARITY           INT NOT NULL,
   PRIMARY KEY ( NEWS_DAY, TOPIC),
   INDEX ( DAY_OF_WEEK, TOPIC ),
   INDEX ( TOPIC )
);

CREATE TABLE IF NOT EXISTS AGGREGATE_TAG (
   NEWS_DAY             VARCHAR(8) NOT NULL,
   SORT_YEAR                 VARCHAR(4) NOT NULL,
   SORT_MONTH                VARCHAR(2) NOT NULL,
   SORT_DAY                  VARCHAR(2) NOT NULL,
   DAY_OF_WEEK          VARCHAR(3) NOT NULL,
   TAG             VARCHAR(30) NOT NULL,
   NEWS_COUNT           INT NOT NULL,
   POPULARITY           INT NOT NULL,
   PRIMARY KEY ( NEWS_DAY, TAG ),
   INDEX ( DAY_OF_WEEK, TAG ),
   INDEX ( TAG )
);

CREATE TABLE IF NOT EXISTS AGGREGATE_INTERACTION (
   INTERACTION_DAY             VARCHAR(8) NOT NULL,
   DAY_OF_WEEK                 VARCHAR(3) NOT NULL,
   NEWS_METADATA_KEY           VARCHAR(20) NOT NULL,
   NEWS_METADATA_VALUE         VARCHAR(100) NOT NULL,
   PREVIOUS_METADATA_VALUE     VARCHAR(100) NOT NULL,
   INTERACTION_COUNT           INT NOT NULL,
   PRIMARY KEY ( INTERACTION_DAY, NEWS_METADATA_KEY, NEWS_METADATA_VALUE ),
   INDEX ( DAY_OF_WEEK, NEWS_METADATA_KEY, NEWS_METADATA_VALUE )
);

CREATE TABLE IF NOT EXISTS NEWS (
   NEWS_UUID              VARCHAR(100) NOT NULL UNIQUE,
   NEWS_DAY               VARCHAR(8) NOT NULL,
   DAY_OF_WEEK            VARCHAR(3) NOT NULL,
   NEWS_TITLE             VARCHAR(100) NOT NULL,
   NEWS_CONTEXT           LONGTEXT NOT NULL,
   CATEGORY               VARCHAR(30) NOT NULL,
   RATING                 INT NOT NULL,
   POPULARITY              INT NOT NULL,
   PRIMARY KEY ( NEWS_UUID ),
   INDEX ( NEWS_DAY ),
   INDEX ( DAY_OF_WEEK ),
   INDEX ( CATEGORY )

);

CREATE TABLE IF NOT EXISTS NEWS_MAP (
   NEWS_MAP_UUID             VARCHAR(100) NOT NULL,
   NEWS_UUID             VARCHAR(100) NOT NULL,
   NEWS_METADATA_KEY     VARCHAR(20) NOT NULL,
   NEWS_METADATA_VALUE   VARCHAR(100) NOT NULL,
   PRIMARY KEY ( NEWS_MAP_UUID ),
   INDEX ( NEWS_UUID ) ,
   INDEX ( NEWS_METADATA_KEY ),
   INDEX ( NEWS_METADATA_VALUE ),
   INDEX ( NEWS_METADATA_KEY, NEWS_METADATA_VALUE )
);
