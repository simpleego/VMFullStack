-- 학습용 DB 생성 (한글/이모지를 위해 utf8mb4 사용)
CREATE DATABASE IF NOT EXISTS vmShop
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

-- 프로젝트 전용 계정 (root를 직접 쓰지 않기 위함)
-- 비밀번호는 학습용 예시이므로 실제 서비스에서는 사용하지 않는다
CREATE USER IF NOT EXISTS 'vmshop_user'@'localhost' IDENTIFIED BY 'vmshop1234';
GRANT ALL PRIVILEGES ON vmShop.* TO 'vmshop_user'@'localhost';
FLUSH PRIVILEGES;
