BEGIN TRANSACTION;

-- Ensure table exists with validation and a uniqueness constraint
CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    name TEXT NOT NULL,
    min_score INTEGER NOT NULL CHECK (min_score >= 0),
    min_income INTEGER NOT NULL CHECK (min_income >= 0),
    age_req INTEGER NOT NULL CHECK (age_req >= 0),
    cashback_min REAL DEFAULT 0 CHECK (cashback_min >= 0),
    cashback_max REAL DEFAULT 0 CHECK (cashback_max >= 0),
    apr_min REAL DEFAULT 0 CHECK (apr_min >= 0),
    apr_max REAL DEFAULT 0 CHECK (apr_max >= 0),
    annual_fee REAL DEFAULT 0 CHECK (annual_fee >= 0),
    ref TEXT NOT NULL,
    UNIQUE(company, name)
);

-- Useful indexes for lookups
CREATE INDEX IF NOT EXISTS idx_cards_company ON cards(company);
CREATE INDEX IF NOT EXISTS idx_cards_min_score ON cards(min_score);

-- Seed data (won't duplicate due to UNIQUE + OR IGNORE)
INSERT OR IGNORE INTO cards (company, name, min_score, min_income, age_req, cashback_min, cashback_max, apr_min, apr_max, annual_fee, ref) VALUES
('Chase', 'Ink Business Unlimited', 670, 0, 18, 1.5, 1.5, 18.24, 24.24, 0, 'https://creditcards.chase.com/business-credit-cards/ink/unlimited'),
('Chase', 'Sapphire Preferred', 700, 0, 18, 0, 0, 21.24, 28.24, 95, 'https://creditcards.chase.com/rewards-credit-cards/sapphire/preferred?iCELL=61FY'),
('Chase', 'Ink Business Premier', 700, 0, 18, 2.0, 2.5, 19.24, 25.24, 195, 'https://creditcards.chase.com/business-credit-cards/ink/premier'),
('Chase', 'Ink Business Cash', 670, 0, 18, 1.0, 5.0, 18.24, 24.24, 0, 'https://creditcards.chase.com/business-credit-cards/ink/cash'),
('Chase', 'Sapphire Reserve for Business', 740, 0, 18, 3.0, 3.0, 22.24, 29.24, 550, 'https://creditcards.chase.com/business-credit-cards/sapphire/reserve'),
('Chase', 'Ink Business Preferred', 700, 0, 18, 3.0, 3.0, 20.24, 26.24, 95, 'https://creditcards.chase.com/business-credit-cards/ink/preferred'),
('Chase', 'Chase Freedom', 670, 0, 18, 1.5, 5.0, 20.24, 28.99, 0, 'https://creditcards.chase.com/rewards-credit-cards/chase-freedom');

COMMIT;
