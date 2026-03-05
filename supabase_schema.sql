-- ============================================
-- DIET TRACKER FIT - BASE DE DATOS COMPLETA
-- Supabase: kaomgwojvnncidyezdzj
-- ============================================

-- 1. USER PROFILES
CREATE TABLE IF NOT EXISTS user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  age INTEGER,
  gender TEXT CHECK (gender IN ('male', 'female', 'other')),
  height_cm INTEGER,
  weight_kg DECIMAL(5,2),
  activity_level TEXT CHECK (activity_level IN ('sedentary', 'light', 'moderate', 'active', 'very_active')),
  goal TEXT CHECK (goal IN ('lose', 'maintain', 'gain')),
  target_weight_kg DECIMAL(5,2),
  allergies TEXT[],
  daily_calories INTEGER,
  tdee INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. MASTER RECIPES (200 recetas)
CREATE TABLE IF NOT EXISTS master_recipes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  meal_type TEXT CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
  supermarket TEXT CHECK (supermarket IN ('mercadona', 'lidl', 'carrefour', 'generic')),
  calories INTEGER NOT NULL,
  protein_g DECIMAL(6,2) NOT NULL,
  carbs_g DECIMAL(6,2) NOT NULL,
  fat_g DECIMAL(6,2) NOT NULL,
  fiber_g DECIMAL(6,2),
  ingredients JSONB,
  instructions TEXT,
  prep_time_min INTEGER,
  servings INTEGER DEFAULT 1,
  image_url TEXT,
  rating DECIMAL(3,2) DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. WEEKLY PLANS
CREATE TABLE IF NOT EXISTS weekly_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  week_start DATE NOT NULL,
  week_end DATE NOT NULL,
  total_calories INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, week_start)
);

-- 4. PLAN MEALS
CREATE TABLE IF NOT EXISTS plan_meals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plan_id UUID REFERENCES weekly_plans(id) ON DELETE CASCADE,
  day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6),
  meal_type TEXT CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
  recipe_id UUID REFERENCES master_recipes(id),
  servings INTEGER DEFAULT 1,
  calories INTEGER,
  protein_g DECIMAL(6,2),
  carbs_g DECIMAL(6,2),
  fat_g DECIMAL(6,2),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. WEIGHT LOGS
CREATE TABLE IF NOT EXISTS weight_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  weight_kg DECIMAL(5,2) NOT NULL,
  body_fat_pct DECIMAL(4,2),
  logged_at DATE DEFAULT CURRENT_DATE,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. SHOPPING LISTS
CREATE TABLE IF NOT EXISTS shopping_lists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  recipe_id UUID REFERENCES master_recipes(id),
  ingredient TEXT NOT NULL,
  quantity TEXT,
  unit TEXT,
  checked BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. FOOD LOGS (diario de comidas)
CREATE TABLE IF NOT EXISTS food_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  food_name TEXT NOT NULL,
  calories INTEGER NOT NULL,
  protein_g DECIMAL(6,2),
  carbs_g DECIMAL(6,2),
  fat_g DECIMAL(6,2),
  logged_at DATE DEFAULT CURRENT_DATE,
  meal_type TEXT CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
  recipe_id UUID REFERENCES master_recipes(id),
  servings DECIMAL(4,2) DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ÍNDICES PARA PERFORMANCE
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(id);
CREATE INDEX IF NOT EXISTS idx_master_recipes_meal_type ON master_recipes(meal_type);
CREATE INDEX IF NOT EXISTS idx_master_recipes_supermarket ON master_recipes(supermarket);
CREATE INDEX IF NOT EXISTS idx_master_recipes_calories ON master_recipes(calories);
CREATE INDEX IF NOT EXISTS idx_weekly_plans_user_id ON weekly_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_plan_meals_plan_id ON plan_meals(plan_id);
CREATE INDEX IF NOT EXISTS idx_weight_logs_user_id ON weight_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_weight_logs_logged_at ON weight_logs(logged_at);
CREATE INDEX IF NOT EXISTS idx_shopping_lists_user_id ON shopping_lists(user_id);
CREATE INDEX IF NOT EXISTS idx_food_logs_user_id ON food_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_food_logs_logged_at ON food_logs(logged_at);

-- ROW LEVEL SECURITY (RLS)
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE master_recipes ENABLE ROW LEVEL SECURITY;
ALTER TABLE weekly_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE plan_meals ENABLE ROW LEVEL SECURITY;
ALTER TABLE weight_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE shopping_lists ENABLE ROW LEVEL SECURITY;
ALTER TABLE food_logs ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view own profile" ON user_profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON user_profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON user_profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "Anyone can view recipes" ON master_recipes FOR SELECT USING (true);
CREATE POLICY "Users can view own plans" ON weekly_plans FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create own plans" ON weekly_plans FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own plans" ON weekly_plans FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own plans" ON weekly_plans FOR DELETE USING (auth.uid() = user_id);
CREATE POLICY "Users can view own weight logs" ON weight_logs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own weight logs" ON weight_logs FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own weight logs" ON weight_logs FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own weight logs" ON weight_logs FOR DELETE USING (auth.uid() = user_id);
CREATE POLICY "Users can view own shopping lists" ON shopping_lists FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can manage own shopping lists" ON shopping_lists FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can view own food logs" ON food_logs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own food logs" ON food_logs FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own food logs" ON food_logs FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own food logs" ON food_logs FOR DELETE USING (auth.uid() = user_id);

-- Función para calcular calorías diarias (Mifflin-St Jeor)
CREATE OR REPLACE FUNCTION calculate_daily_calories(
  age INTEGER, gender TEXT, height_cm INTEGER, weight_kg DECIMAL, activity_level TEXT, goal TEXT
) RETURNS INTEGER AS $$
DECLARE tmb INTEGER; tdee INTEGER;
BEGIN
  IF gender = 'male' THEN tmb := (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5;
  ELSE tmb := (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161; END IF;
  CASE activity_level
    WHEN 'sedentary' THEN tdee := tmb * 1.2;
    WHEN 'light' THEN tdee := tmb * 1.375;
    WHEN 'moderate' THEN tdee := tmb * 1.55;
    WHEN 'active' THEN tdee := tmb * 1.725;
    WHEN 'very_active' THEN tdee := tmb * 1.9;
    ELSE tdee := tmb * 1.2;
  END CASE;
  CASE goal WHEN 'lose' THEN RETURN tdee - 500; WHEN 'gain' THEN RETURN tdee + 500; ELSE RETURN tdee; END CASE;
END;
$$ LANGUAGE plpgsql;
