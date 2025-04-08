-- seed.sql

INSERT INTO users (username, email, password_hash)
VALUES 
  ('admin', 'admin@example.com', 'hashed_pw1'),
  ('testuser', 'test@example.com', 'hashed_pw2');
