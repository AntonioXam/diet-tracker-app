-- Fix: La columna salt en users debe ser nullable o usar valor por defecto
ALTER TABLE users ALTER COLUMN salt DROP NOT NULL;

-- O alternativamente, añadir default
ALTER TABLE users ALTER COLUMN salt SET DEFAULT '';

-- Verificar estructura
SELECT column_name, data_type, is_nullable FROM information_schema.columns 
WHERE table_name = 'users';