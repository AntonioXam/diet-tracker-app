-- Migration: Add missing columns to user_profiles table
-- Database: Supabase - kaomgwojvnncidyezdzj
-- Date: 2026-03-06

-- Execute this SQL in Supabase Dashboard > SQL Editor:
-- https://supabase.com/dashboard/project/kaomgwojvnncidyezdzj/sql/new

ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS budget VARCHAR(20) DEFAULT 'medium';
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS meals_per_day INTEGER DEFAULT 4;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS target_calories INTEGER;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS preferences TEXT;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE;

-- Verify the columns were added:
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'user_profiles' 
AND column_name IN ('budget', 'meals_per_day', 'target_calories', 'preferences', 'onboarding_completed')
ORDER BY column_name;