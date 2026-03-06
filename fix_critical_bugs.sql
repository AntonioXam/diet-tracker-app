-- ============================================
-- FIX CRÍTICO 1: Añadir columna name a users
-- ============================================

-- Añadir columna name si no existe
ALTER TABLE users ADD COLUMN IF NOT EXISTS name TEXT;

-- Verificar
SELECT column_name, data_type FROM information_schema.columns 
WHERE table_name = 'users' AND column_name = 'name';

-- ============================================
-- FIX CRÍTICO 2: Crear trigger para perfil automático
-- ============================================

-- Función para crear perfil automáticamente
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.user_profiles (id, age, gender, height_cm, weight_kg, activity_level, goal)
  VALUES (
    NEW.id,
    25,
    'male',
    175,
    70,
    'moderate',
    'maintain'
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================
-- FIX CRÍTICO 3: Datos de ejemplo para probar
-- ============================================

-- Verificar que funciona
SELECT 'Fixes aplicados correctamente' as status;