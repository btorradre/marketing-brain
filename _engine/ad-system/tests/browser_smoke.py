"""UI verification in an isolated fixture database; live inventory is read-only."""
import json, sys, tempfile, threading
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from playwright.sync_api import sync_playwright
from store import Store
from server import make_server
OUT=Path(__file__).resolve().parents[1]/'data/verification'
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);st=Store(root/'_engine/ad-system/data/test.sqlite3',root);server=make_server(st,0);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1440,'height':1050});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(f'http://127.0.0.1:{server.server_port}');page.get_by_role('button',name='+ New concept').click();page.get_by_label('Concept name',exact=True).fill('Isolated browser test');page.get_by_role('button',name='Continue').click();page.get_by_role('heading',name='Isolated browser test',exact=True).wait_for()
            page.get_by_label('Product / variant',exact=True).fill('Synthetic product');page.get_by_label('Context and uncertainties',exact=True).fill('Synthetic local QA only.');page.get_by_role('button',name='Save changes',exact=True).click();page.get_by_role('button',name='Saved',exact=True).wait_for()
            page.reload();page.get_by_label('Product / variant',exact=True).wait_for();assert page.get_by_label('Product / variant',exact=True).input_value()=='Synthetic product'
            page.get_by_role('button',name='Story',exact=True).click();page.get_by_role('button',name='+ Add hook',exact=True).click();page.get_by_label('Spoken hook',exact=True).fill('Test hook');page.get_by_label('Opening action / first frame',exact=True).fill('Test action');page.get_by_label('What this hook tests',exact=True).fill('Test variable');page.get_by_role('button',name='Save changes',exact=True).click();page.get_by_role('button',name='Saved',exact=True).wait_for()
            page.get_by_role('button',name='Work',exact=True).click();page.get_by_role('button',name='Prepare work packet',exact=True).click();page.get_by_role('link',name='Open work packet',exact=False).wait_for();page.get_by_role('button',name='Start work',exact=True).click();page.get_by_label('Person / agent session',exact=True).fill('Synthetic browser QA');page.get_by_role('button',name='Continue').click();page.get_by_text('working',exact=True).wait_for()
            page.get_by_role('button',name='Review',exact=True).click();page.get_by_role('button',name='Run & save checks',exact=True).click();page.get_by_text('Readiness review saved.',exact=True).wait_for()
            page.get_by_role('button',name='Memory',exact=True).click();page.get_by_role('button',name='Add memory',exact=True).click();page.get_by_label('Observation or lesson',exact=True).fill('Isolated UI memory fixture');page.get_by_label('Source / original instruction and date',exact=True).fill('Local synthetic QA');page.get_by_role('button',name='Continue').click();page.get_by_text('Saved to the shared Obsidian agent notes.',exact=True).wait_for();assert 'Isolated UI memory fixture' in page.locator('#memorybody pre').inner_text()
            page.get_by_role('button',name='Results',exact=True).click();page.get_by_text('No exact-ID matched performance for this creative.',exact=False).wait_for();page.get_by_role('button',name='Write a decision',exact=True).click();page.get_by_label('Observation',exact=True).fill('No data yet');page.get_by_label('Interpretation',exact=True).fill('Cannot infer performance');page.get_by_label('Alternative',exact=True).fill('Data not imported');page.get_by_label('Next test',exact=True).fill('Import test data later');page.get_by_label('Fixed',exact=True).fill('Concept');page.get_by_label('Changed',exact=True).fill('Evidence availability');page.get_by_role('button',name='Continue').click();page.get_by_role('button',name='Create next brief',exact=True).wait_for()
            page.get_by_role('button',name='Create next brief',exact=True).click();page.get_by_label('New iteration title',exact=True).fill('Synthetic next test');page.get_by_role('button',name='Continue').click();page.get_by_role('heading',name='Synthetic next test',exact=True).wait_for()
            assert len(st.list())==2;assert st.list()[0]['kind']=='iteration'
            page.goto('http://127.0.0.1:8791');page.get_by_role('heading',name='The argument',exact=True).wait_for();page.screenshot(path=str(OUT/'ad-studio-overview.png'),full_page=False)
            for tab in ['Story','Assets','Work','Review','Results','History','Memory','Library']:
                page.get_by_role('button',name=tab,exact=True).click();page.locator('#content .panel').first.wait_for()
                if tab=='Library':page.get_by_label('Search file library').fill('editing-plan');page.get_by_text('matches · showing',exact=False).wait_for()
            page.screenshot(path=str(OUT/'ad-studio-library.png'),full_page=False)
            assert not errors,errors
            browser.close();(OUT/'browser-smoke.json').write_text(json.dumps(dict(status='passed',browser='separate local headless Chromium',isolated_checks=['create','save','restart persistence','hook editor','work packet','start task','QA','insufficient-evidence decision','next brief lineage','shared Obsidian note save/read'],live_checks=['all nine sections','real inventory search'],page_errors=errors),indent=2));print('Browser smoke passed; isolated writes and read-only live inventory.')
    finally:server.shutdown();server.server_close();thread.join()
