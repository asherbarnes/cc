CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    name TEXT NOT NULL,
    min_score INTEGER NOT NULL,
    min_income INTEGER NOT NULL,
    age_req INTEGER NOT NULL,
    cashback FLOAT,
    annual_fee FLOAT,
    ref TEXT NOT NULL
);

INSERT INTO cards (company, name, min_score, min_income, age_req, cashback, annual_fee, ref) VALUES
('Chase', 'Ink Business Unlimited', 670, 0, 18, 1.5, 0, 'https://creditcards.chase.com/business-credit-cards/ink/unlimited'),
('Chase', 'Sapphire Preferred', 700, 0, 18, 0, 95, 'https://creditcards.chase.com/rewards-credit-cards/sapphire/preferred?iCELL=61FY');
