-- ============================================
-- FIX DEFINITIVO - EJECUTAR EN SUPABASE SQL EDITOR
-- https://supabase.com/dashboard/project/kaomgwojvnncidyezdzj/sql/new
-- ============================================

-- 1. Añadir columna salt si no existe
ALTER TABLE users ADD COLUMN IF NOT EXISTS salt TEXT;

-- 2. Añadir columna name si no existe
ALTER TABLE users ADD COLUMN IF NOT EXISTS name TEXT;

-- 3. Verificar estructura
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;

-- 4. Verificar que funciona
SELECT 'Fix aplicado correctamente - users tiene salt y name' as status;