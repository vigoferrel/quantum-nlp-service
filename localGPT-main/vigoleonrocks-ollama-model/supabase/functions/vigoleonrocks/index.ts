// @ts-nocheck
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

// Los secrets se obtienen automáticamente del entorno de Supabase
const supabaseUrl = Deno.env.get('SUPABASE_URL')!
const supabaseKey = Deno.env.get('SUPABASE_ANON_KEY')!
const supabase = createClient(supabaseUrl, supabaseKey)

serve(async (req) => {
  try {
    const { prompt, context } = await req.json()
    
    // Quantum-Cognitive Processing
    const { data, error } = await supabase
      .rpc('vigoleonrocks_inference', {
        prompt,
        context: context || '',
        model_config: 'quantum-xl'
      })

    if (error) {
      console.error('Error in RPC call:', error)
      throw error
    }

    return new Response(
      JSON.stringify(data),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (err) {
    console.error('Error in function:', err)
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    )
  }
})