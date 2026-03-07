# Database Migration Note

To support the new food logging features, the `food_logs` table in Supabase needs the following columns (if they don't exist):

```sql
-- Run this in Supabase SQL Editor if columns don't exist
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS food_name TEXT;
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS barcode TEXT;
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS source TEXT DEFAULT 'manual';
ALTER TABLE food_logs ADD COLUMN IF NOT EXISTS quantity FLOAT DEFAULT 1;

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_food_logs_user_date ON food_logs(user_id, week_number, day_of_week);
```

The food_logs table should have these columns:
- id (uuid, primary key)
- user_id (uuid, references users)
- recipe_id (uuid, optional - references master_recipes)
- food_name (text, optional - for manual/Open Food Facts entries)
- barcode (text, optional - for scanned products)
- meal_type (text)
- calories (float)
- protein (float)
- carbs (float)
- fat (float)
- quantity (float, default 1)
- source (text - 'plan', 'manual', 'openfoodfacts')
- notes (text)
- week_number (integer)
- day_of_week (integer)
- logged_at (timestamp)
- created_at (timestamp)
