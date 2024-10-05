-- Authors Table
CREATE TABLE Authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    `index` INT UNIQUE NOT NULL,  -- Unique index for the author
    last_name VARCHAR(255) NOT NULL,
    given_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    affiliation VARCHAR(255),
    interests TEXT
);

-- Profiles Table (Linked to Authors)
CREATE TABLE Profiles (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    profile_type VARCHAR(255) NOT NULL,  -- e.g., Google Scholar, DBLP, ACM
    profile_url VARCHAR(255),
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE
);

-- Publications Table
CREATE TABLE Publications (
    publication_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    title_url VARCHAR(255),
    journal_info VARCHAR(255),
    doi VARCHAR(255) UNIQUE NOT NULL,  -- Ensuring DOI uniqueness
    abstract TEXT
);

-- Publication Metrics Table
CREATE TABLE Publication_Metrics (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    publication_id INT,
    citations INT,
    downloads_6_weeks INT,
    downloads_12_months INT,
    downloads_cumulative INT,
    FOREIGN KEY (publication_id) REFERENCES Publications(publication_id) ON DELETE CASCADE
);

-- Co-Authors Table (Many-to-Many linking authors and publications)
CREATE TABLE Co_Authors (
    author_publication_id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    publication_id INT,
    is_primary_author BOOLEAN,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE,
    FOREIGN KEY (publication_id) REFERENCES Publications(publication_id) ON DELETE CASCADE
);

-- Bibliometrics Table
CREATE TABLE Bibliometrics (
    bibliometric_id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    average_citation_per_article FLOAT,
    citation_count INT,
    publication_counts INT,
    publication_years VARCHAR(50),  -- e.g., "2000-2023"
    average_downloads_per_article FLOAT,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE
);

-- Keywords Table
CREATE TABLE Keywords (
    keyword_id INT AUTO_INCREMENT PRIMARY KEY,
    publication_id INT,
    term VARCHAR(255) NOT NULL,  -- The keyword itself
    label VARCHAR(255),
    count INT,  -- Number of occurrences of this keyword
    FOREIGN KEY (publication_id) REFERENCES Publications(publication_id) ON DELETE CASCADE
);

-- Awards Table (Linked to Authors)
CREATE TABLE Awards (
    award_id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    award_name VARCHAR(255) NOT NULL,
    year_won INT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE
);

-- Bar Chart Data Table (Yearly metrics for visualizations)
CREATE TABLE Bar_Chart_Data (
    chart_data_id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    year INT NOT NULL,  -- Year for the data point
    count INT,  -- Count of publications or metrics for that year
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE
);

-- Author_Keywords Table (Many-to-Many linking authors and keywords)
CREATE TABLE Author_Keywords (
    author_id INT,
    keyword_id INT,
    PRIMARY KEY (author_id, keyword_id),  -- Composite primary key
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES Keywords(keyword_id) ON DELETE CASCADE
);
