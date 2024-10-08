
CREATE TABLE Authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    `index` INT UNIQUE NOT NULL,  
    last_name VARCHAR(255) NOT NULL,
    given_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    affiliation VARCHAR(255),
    interests TEXT
);


CREATE TABLE Profiles (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    profile_type VARCHAR(255) NOT NULL,  
    profile_url VARCHAR(255),
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE
);


CREATE TABLE Publications (
    publication_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    title_url VARCHAR(255),
    journal_info VARCHAR(255),
    doi VARCHAR(255) UNIQUE NOT NULL,  
    abstract TEXT
);


CREATE TABLE Publication_Metrics (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    publication_id INT,
    citations INT,
    downloads_6_weeks INT,
    downloads_12_months INT,
    downloads_cumulative INT,
    FOREIGN KEY (publication_id) REFERENCES Publications(publication_id) ON DELETE CASCADE
);


CREATE TABLE Co_Authors (
    author_publication_id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    publication_id INT,
    is_primary_author BOOLEAN,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE,
    FOREIGN KEY (publication_id) REFERENCES Publications(publication_id) ON DELETE CASCADE
);


CREATE TABLE Bibliometrics (
    bibliometric_id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    average_citation_per_article FLOAT,
    citation_count INT,
    publication_counts INT,
    publication_years VARCHAR(50),  
    average_downloads_per_article FLOAT,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE
);

CREATE TABLE Keywords (
    keyword_id INT AUTO_INCREMENT PRIMARY KEY,
    publication_id INT,
    term VARCHAR(255) NOT NULL, 
    label VARCHAR(255),
    count INT,  
    FOREIGN KEY (publication_id) REFERENCES Publications(publication_id) ON DELETE CASCADE
);


CREATE TABLE Awards (
    award_id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    award_name VARCHAR(255) NOT NULL,
    year_won INT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE
);

CREATE TABLE Bar_Chart_Data (
    chart_data_id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    year INT NOT NULL, 
    count INT,  
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE
);


CREATE TABLE Author_Keywords (
    author_id INT,
    keyword_id INT,
    PRIMARY KEY (author_id, keyword_id), 
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES Keywords(keyword_id) ON DELETE CASCADE
);
