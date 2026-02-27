import sys, os, traceback
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')
sys.path.insert(0, 'backend')

tests = [
    ('auth_routes',      'from backend.routes.auth_routes import router'),
    ('api_routes',       'from backend.routes.api_routes import router'),
    ('linkedin_jobs',    'from backend.routes.linkedin_jobs_routes import router'),
    ('agent_routes',     'from backend.routes.agent_routes import router'),
    ('ats_routes',       'from backend.routes.ats_routes import router'),
    ('cover_letter',     'from backend.routes.cover_letter_routes import router'),
    ('autoagenthire',    'from backend.api.autoagenthire import router'),
    ('v2_routes',        'from backend.routes.v2_routes import router'),
    ('full_app',         'from backend.main import app'),
]
for name, stmt in tests:
    try:
        exec(stmt)
        print(f'OK  {name}')
    except Exception as e:
        print(f'ERR {name}: {type(e).__name__}: {e}')
        traceback.print_exc()
    sys.stdout.flush()

# Now check routes registered in the app
try:
    from backend.main import app as the_app
    routes = [r.path for r in the_app.routes]
    print(f'\nRegistered routes ({len(routes)}):')
    for r in sorted(routes):
        print(f'  {r}')
except Exception as e:
    print(f'Could not inspect app routes: {e}')
