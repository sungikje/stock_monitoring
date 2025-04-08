-- seed.sql

INSERT INTO users (username, email, password_hash)
VALUES 
  ('admin', 'admin@example.com', 'hashed_pw1'),
  ('testuser', 'test@example.com', 'hashed_pw2');


INSERT INTO user_favorite_companies (user_id, company_name, industry_period, base_price)
VALUES 
  (1, '삼성전자', 12, 70000),
  (1, '카카오', 12, 55000);