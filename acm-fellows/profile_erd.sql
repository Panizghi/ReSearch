CREATE TABLE Author_Keywords
(
  author_id  INT,
  keyword_id INT,
  ON            ,
  ON            ,
  PRIMARY KEY (author_id, keyword_id)
);

CREATE TABLE Authors
(
  author_id   INT          GENERATED ALWAYS AS IDENTITY,
  NULL                     UNIQUE,
  last_name   VARCHAR(255) NOT NULL,
  given_name  VARCHAR(255) NOT NULL,
  location    VARCHAR(255),
  affiliation VARCHAR(255),
  interests   TEXT        ,
  PRIMARY KEY (author_id)
);

CREATE TABLE Awards
(
  award_id   INT          GENERATED ALWAYS AS IDENTITY,
  author_id  INT         ,
  award_name VARCHAR(255) NOT NULL,
  year_won   INT          NOT NULL,
  ON                     ,
  PRIMARY KEY (award_id)
);

CREATE TABLE Bar_Chart_Data
(
  chart_data_id INT GENERATED ALWAYS AS IDENTITY,
  author_id     INT,
  year          INT NOT NULL,
  count         INT,
  ON               ,
  PRIMARY KEY (chart_data_id)
);

CREATE TABLE Bibliometrics
(
  bibliometric_id               INT         GENERATED ALWAYS AS IDENTITY,
  author_id                     INT        ,
  average_citation_per_article  FLOAT      ,
  citation_count                INT        ,
  publication_counts            INT        ,
  publication_years             VARCHAR(50),
  average_downloads_per_article FLOAT      ,
  ON                                       ,
  PRIMARY KEY (bibliometric_id)
);

CREATE TABLE Co_Authors
(
  author_publication_id INT     GENERATED ALWAYS AS IDENTITY,
  author_id             INT    ,
  publication_id        INT    ,
  is_primary_author     BOOLEAN,
  ON                           ,
  ON                           ,
  PRIMARY KEY (author_publication_id)
);

CREATE TABLE Keywords
(
  keyword_id     INT          GENERATED ALWAYS AS IDENTITY,
  publication_id INT         ,
  term           VARCHAR(255) NOT NULL,
  label          VARCHAR(255),
  count          INT         ,
  ON                         ,
  PRIMARY KEY (keyword_id)
);

CREATE TABLE Profiles
(
  profile_id   INT          GENERATED ALWAYS AS IDENTITY,
  author_id    INT         ,
  profile_type VARCHAR(255) NOT NULL,
  profile_url  VARCHAR(255),
  ON                       ,
  PRIMARY KEY (profile_id)
);

CREATE TABLE Publication_Metrics
(
  metric_id            INT GENERATED ALWAYS AS IDENTITY,
  publication_id       INT,
  citations            INT,
  downloads_6_weeks    INT,
  downloads_12_months  INT,
  downloads_cumulative INT,
  ON                      ,
  PRIMARY KEY (metric_id)
);

CREATE TABLE Publications
(
  publication_id INT          GENERATED ALWAYS AS IDENTITY,
  title          VARCHAR(255) NOT NULL,
  title_url      VARCHAR(255),
  journal_info   VARCHAR(255),
  doi            VARCHAR(255) UNIQUE,
  abstract       TEXT        ,
  award_id       INT          NOT NULL,
  PRIMARY KEY (publication_id)
);

ALTER TABLE Profiles
  ADD CONSTRAINT FK_Authors_TO_Profiles
    FOREIGN KEY (author_id)
    REFERENCES Authors (author_id);

ALTER TABLE Publication_Metrics
  ADD CONSTRAINT FK_Publications_TO_Publication_Metrics
    FOREIGN KEY (publication_id)
    REFERENCES Publications (publication_id);

ALTER TABLE Co_Authors
  ADD CONSTRAINT FK_Authors_TO_Co_Authors
    FOREIGN KEY (author_id)
    REFERENCES Authors (author_id);

ALTER TABLE Co_Authors
  ADD CONSTRAINT FK_Publications_TO_Co_Authors
    FOREIGN KEY (publication_id)
    REFERENCES Publications (publication_id);

ALTER TABLE Bibliometrics
  ADD CONSTRAINT FK_Authors_TO_Bibliometrics
    FOREIGN KEY (author_id)
    REFERENCES Authors (author_id);

ALTER TABLE Keywords
  ADD CONSTRAINT FK_Publications_TO_Keywords
    FOREIGN KEY (publication_id)
    REFERENCES Publications (publication_id);

ALTER TABLE Awards
  ADD CONSTRAINT FK_Authors_TO_Awards
    FOREIGN KEY (author_id)
    REFERENCES Authors (author_id);

ALTER TABLE Bar_Chart_Data
  ADD CONSTRAINT FK_Authors_TO_Bar_Chart_Data
    FOREIGN KEY (author_id)
    REFERENCES Authors (author_id);

ALTER TABLE Author_Keywords
  ADD CONSTRAINT FK_Authors_TO_Author_Keywords
    FOREIGN KEY (author_id)
    REFERENCES Authors (author_id);

ALTER TABLE Author_Keywords
  ADD CONSTRAINT FK_Keywords_TO_Author_Keywords
    FOREIGN KEY (keyword_id)
    REFERENCES Keywords (keyword_id);

ALTER TABLE Publications
  ADD CONSTRAINT FK_Awards_TO_Publications
    FOREIGN KEY (award_id)
    REFERENCES Awards (award_id);